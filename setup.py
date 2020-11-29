# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-11-28 10:38:36'


import os
import sys
import requests
from setuptools import setup, find_packages
from QBinder.constant import VERSION
if sys.version_info[0] < 3:
    from codecs import open

# # NOTE 将markdown格式转换为rst格式
# def md_to_rst(from_file, to_file):
#     r = requests.post(url='http://c.docverter.com/convert',
#                       data={'to':'rst','from':'markdown'},
#                       files={'input_files[]':open(from_file,'rb')})
#     if r.ok:
#         with open(to_file, "wb") as f:
#             f.write(r.content)

# md_to_rst("README.md", "README.rst")
# if os.path.exists('README.rst'):
#     long_description = open('README.rst', encoding="utf-8").read()
# else:
# 	long_description = 'Global Data Binding for Python Qt framework'

long_description = "Global Data Binding for Python Qt framework"

setup(
    name="QBinder",
    version=VERSION,
    keywords=("pip", "PyQt", "PySide", "Qt", "DataBinding", "Binding", "Binder"),
    description="Global Data Binding for Python Qt framework",
    long_description=long_description,
    license="MIT Licence",
    url="https://github.com/FXTD-ODYSSEY/QBinder",
    author="timmyliang",
    author_email="820472580@qq.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[
        "PySide2",
        "six",
        "Qt.py",
    ],
)