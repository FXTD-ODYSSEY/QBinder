class QSettingsManager(QObject):

    # Signals
    updated = Signal(int)  # Triggered anytime configuration is changed (refresh)

    def __init__(self, defaults={}, *args, **kwargs):
        super(ConfigManagerBase, self).__init__(*args, **kwargs)

        self.mutex = QMutex()
        self.hooks = HOOKS
        self.reset()
        
        self.defaults = defaults  # Same mapping as above, used when config not set

    def _get_default(self, key):
        with QMutexLocker(self.mutex):
            try:
                return self.defaults[key]
            except:
                return None

    # Get config
    def get(self, key):
        """ 
            Get config value for a given key from the config manager.
            
            Returns the value that matches the supplied key. If the value is not set a
            default value will be returned as set by set_defaults.
            
            :param key: The configuration key to return a config value for
            :type key: str
            :rtype: Any supported (str, int, bool, list-of-supported-types)
        """
        v = self._get(key)
        if v is not None:
            return v
        else:
            return self._get_default(key)

    def set(self, key, value, trigger_handler=True, trigger_update=True):
        """ 
            Set config value for a given key in the config manager.
            
            Set key to value. The optional trigger_update determines whether event hooks
            will fire for this key (and so re-calculation). It is useful to suppress these
            when updating multiple values for example.
            
            :param key: The configuration key to set
            :type key: str
            :param value: The value to set the configuration key to
            :type value: Any supported (str, int, bool, list-of-supported-types)
            :rtype: bool (success)   
        """
        old = self._get(key)
        if old is not None and old == value:
            return False  # Not updating

        # Set value
        self._set(key, value)

        if trigger_handler and key in self.handlers:
            # Trigger handler to update the view
            getter = self.handlers[key].getter
            setter = self.handlers[key].setter

            if setter and getter() != self._get(key):
                setter(self._get(key))

        # Trigger update notification
        if trigger_update:
            self.updated.emit(self.eventhooks[key] if key in self.eventhooks else RECALCULATE_ALL)

        return True

    # Defaults are used in absence of a set value (use for base settings)
    def set_default(self, key, value, eventhook=RECALCULATE_ALL):
        """
        Set the default value for a given key.
        
        This will be returned if the value is 
        not set in the current config. It is important to include defaults for all 
        possible config values for backward compatibility with earlier versions of a plugin.
        
        :param key: The configuration key to set
        :type key: str
        :param value: The value to set the configuration key to
        :type value: Any supported (str, int, bool, list-of-supported-types)
        :param eventhook: Attach either a full recalculation trigger (default), or a view-only recalculation trigger to these values.
        :type eventhook: int RECALCULATE_ALL, RECALCULATE_VIEWS
        
        """

        self.defaults[key] = value
        self.eventhooks[key] = eventhook
        self.updated.emit(eventhook)

    def set_defaults(self, keyvalues, eventhook=RECALCULATE_ALL):
        """
        Set the default value for a set of keys.
        
        These will be returned if the value is 
        not set in the current config. It is important to include defaults for all 
        possible config values for backward compatibility with earlier versions of a plugin.
        
        :param keyvalues: A dictionary of keys and values to set as defaults
        :type key: dict
        :param eventhook: Attach either a full recalculation trigger (default), or a view-only recalculation trigger to these values.
        :type eventhook: int RECALCULATE_ALL, RECALCULATE_VIEWS
        
        """
        for key, value in list(keyvalues.items()):
            self.defaults[key] = value
            self.eventhooks[key] = eventhook

        # Updating the defaults may update the config (if anything without a config value
        # is set by it; should check)
        self.updated.emit(eventhook)
    # Completely replace current config (wipe all other settings)

    def replace(self, keyvalues, trigger_update=True):
        """
        Completely reset the config with a set of key values.
        
        Note that this does not wipe handlers or triggers (see reset), it simply replaces the values
        in the config entirely. It is the equivalent of unsetting all keys, followed by a
        set_many. Anything not in the supplied keyvalues will revert to default.
        
        :param keyvalues: A dictionary of keys and values to set as defaults
        :type keyvalues: dict
        :param trigger_update: Flag whether to trigger a config update (+recalculation) after all values are set. 
        :type trigger_update: bool
        
        """
        self.config = []
        self.set_many(keyvalues)

    def set_many(self, keyvalues, trigger_update=True):
        """
        Set the value of multiple config settings simultaneously.
        
        This postpones the 
        triggering of the update signal until all values are set to prevent excess signals.
        The trigger_update option can be set to False to prevent any update at all.
            
        :param keyvalues: A dictionary of keys and values to set.
        :type key: dict
        :param trigger_update: Flag whether to trigger a config update (+recalculation) after all values are set. 
        :type trigger_update: bool
        """
        has_updated = False
        for k, v in list(keyvalues.items()):
            u = self.set(k, v, trigger_update=False)
            has_updated = has_updated or u

        if has_updated and trigger_update:
            self.updated.emit(RECALCULATE_ALL)

        return has_updated
    # HANDLERS

    # Handlers are UI elements (combo, select, checkboxes) that automatically update
    # and updated from the config manager. Allows instantaneous updating on config
    # changes and ensuring that elements remain in sync

    def add_handler(self, key, handler, mapper=(lambda x: x, lambda x: x),
                    auto_set_default=True, default=None):
        """
        Add a handler (UI element) for a given config key.
        
        The supplied handler should be a QWidget or QAction through which the user
        can change the config setting. An automatic getter, setter and change-event
        handler is attached which will keep the widget and config in sync. The attached
        handler will default to the correct value from the current config.
        
        An optional mapper may also be provider to handler translation from the values
        shown in the UI and those saved/loaded from the config.

        """
        # Add map handler for converting displayed values to internal config data
        if isinstance(mapper, (dict, OrderedDict)):  # By default allow dict types to be used
            mapper = build_dict_mapper(mapper)

        elif isinstance(mapper, list) and isinstance(mapper[0], tuple):
            mapper = build_tuple_mapper(mapper)

        handler._get_map, handler._set_map = mapper

        # TODO 改良绑定数据
        if key in self.handlers:  # Already there; so skip must remove first to replace
            return

        self.handlers[key] = handler


        # Look for class in hooks and add getter, setter, updater
        cls = self._get_hook(handler)
        hookg, hooks, hooku = self.hooks[cls]

        handler.getter = types_MethodType(hookg, handler)
        handler.setter = types_MethodType(hooks, handler)
        handler.updater = types_MethodType(hooku, handler)

        logging.debug("Add handler %s for %s" % (type(handler).__name__, key))
        handler_callback = lambda x = None: self.set(key, handler.getter(),
                                                     trigger_handler=False)
        handler.updater().connect(handler_callback)

        # Store this so we can issue a specific remove on deletes
        self.handler_callbacks[key] = handler_callback

        # If the key is not in defaults, set the default to match the handler
        if key not in self.defaults:
            if default is None:
                self.set_default(key, handler.getter())
            else:
                self.set_default(key, default)

        # Keep handler and data consistent
        if self._get(key) is not None:
            handler.setter(self._get(key))

        # If the key is in defaults; set the handler to the default state (but don't add to config)
        elif key in self.defaults:
            handler.setter(self.defaults[key])

    def _get_hook(self, handler):
        fst = lambda x: next(x, None)

        cls = fst(x for x in self.hooks.keys() if x == type(handler))
        if cls is None:
            cls = fst(x for x in self.hooks.keys() if isinstance(handler, x))

        if cls is None:
            raise TypeError("No handler-functions available for this widget "
                            "type (%s)" % type(handler).__name__)
        return cls


    def add_handlers(self, keyhandlers):
        for key, handler in list(keyhandlers.items()):
            self.add_handler(key, handler)

    def remove_handler(self, key):
        if key in self.handlers:
            handler = self.handlers[key]
            handler.updater().disconnect(self.handler_callbacks[key])
            del self.handlers[key]

    def add_hooks(self, key, hooks):
        self.hooks[key] = hooks

    def getXMLConfig(self, root):
        config = et.SubElement(root, "Config")
        for ck, cv in list(self.config.items()):
            co = et.SubElement(config, "ConfigSetting")
            co.set("id", ck)
            t = type(cv).__name__
            co.set("type", type(cv).__name__)
            co = CONVERT_TYPE_TO_XML[t](co, cv)

        return root

    def setXMLConfig(self, root):

        config = {}
        for xconfig in root.findall('Config/ConfigSetting'):
            #id="experiment_control" type="unicode" value="monocyte at intermediate differentiation stage (GDS2430_2)"/>
            if xconfig.get('type') in CONVERT_TYPE_FROM_XML:
                v = CONVERT_TYPE_FROM_XML[xconfig.get('type')](xconfig)
            config[xconfig.get('id')] = v

        self.set_many(config, trigger_update=False)

    def as_dict(self):
        '''
        Return the combination of defaults and config as a flat dict (so it can be pickled)
        '''
        result_dict = {}
        for k, v in self.defaults.items():
            result_dict[k] = self.get(k)

        return 
        
    def reset(self):
        """ 
            Reset the config manager to it's initialised state.
            
            This clears all values, unsets all defaults and removes all handlers, maps, and hooks.
        """
        self.config = {}
        self.handlers = {}
        self.handler_callbacks = {}
        self.defaults = {}
        self.maps = {}
        self.eventhooks = {}
        