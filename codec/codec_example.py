# -*- coding: future_fstrings -*-
text = 'hello '
print f"{text} abc"

import codecs
import string

# NOTE https://stackoverflow.com/questions/38777818/how-do-i-properly-create-custom-text-codecs

# prepare map from numbers to letters
_encode_table = {str(number): bytes(letter) for number, letter in enumerate(string.ascii_lowercase)}

# prepare inverse map
_decode_table = {v: k for k, v in _encode_table.items()}


def custom_encode(text):
    # example encoder that converts ints to letters
    print "custom_encode",text
    # see https://docs.python.org/3/library/codecs.html#codecs.Codec.encode
    return b''.join(_encode_table[x] for x in text), len(text)


def custom_decode(binary):
    # example decoder that converts letters to ints
    print "custom_decode",binary
    # see https://docs.python.org/3/library/codecs.html#codecs.Codec.decode
    return ''.join(_decode_table[x] for x in binary), len(binary)


def custom_search_function(encoding_name):
    return codecs.CodecInfo(encode=custom_encode, decode=custom_decode, name='Reasons')


def main():

    # register your custom codec
    # note that CodecInfo.name is used later
    codecs.register(custom_search_function)

    binary = 'abcdefg'
    # decode letters to numbers
    text = binary.decode('Reasons')
    print(text)
    # encode numbers to letters
    binary2 = text.encode('Reasons') 
    print(binary2)

    fstring = 'f"hello {text}"'.decode('future-fstrings')
    print fstring
    # encode(decode(...)) should be an identity function
    assert binary == binary2

if __name__ == '__main__':
    main()