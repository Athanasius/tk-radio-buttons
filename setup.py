#!/usr/bin/env python3

import py2exe
import shutil
from distutils.core import setup
from os.path import isdir

APPNAME = 'edmc-like-tk-radio-buttons'
APP = 'edmc.py'
VERSION = '0.0.1'
COPYRIGHT = '© 2020 Athanasius'

dist_dir = 'dist.win32'

if dist_dir and len(dist_dir) > 1 and isdir(dist_dir):
    shutil.rmtree(dist_dir)


OPTIONS = {
    'py2exe' :
        {
            'dist_dir': dist_dir,
            'optimize': 2
        }
}

setup(
    name=APPNAME,
    version=VERSION,
    windows=[
        {
            'dest_base': APPNAME,
            'script': APP,
            'company_name': 'Miggy',
            'product_name': APPNAME,
            'version': VERSION,
            'product_version': VERSION,
            'copyright': COPYRIGHT,
        }
    ],
    options = OPTIONS,
)