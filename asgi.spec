#
# Wordless: Packaging - spec File
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import os
import platform
import sys

import PyInstaller

block_cipher = None
datas = []

datas.extend(PyInstaller.utils.hooks.collect_data_files('uvicorn'))
datas.extend(PyInstaller.utils.hooks.collect_data_files('sacremoses'))


# Hidden imports
hiddenimports = [
    "uvicorn",
    "uvicorn.logging",
    "uvicorn.loops",
    "uvicorn.loops.auto",
    "uvicorn.protocols"
]

# Runtime hooks
runtime_hooks = [
]

# Exclusions
if platform.system() in ['Windows', 'Linux']:
    excludes = []
elif platform.system() == 'Darwin':
    excludes = [
        'PIL'
    ]

a = Analysis(['asgi.py'],
             pathex = [],
             binaries = [],
             datas = datas,
             hiddenimports = hiddenimports,
             hookspath = [],
             runtime_hooks = runtime_hooks,
             excludes = excludes,
             win_no_prefer_redirects = False,
             win_private_assemblies = False,
             cipher = block_cipher,
             noarchive = False)

pyz = PYZ(a.pure, a.zipped_data,
          cipher = block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries = True,
          name = 'Lyrics',
          debug = False,
          bootloader_ignore_signals = False,
          strip = False,
          upx = True,
          console = False)

# Collect data files
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip = False,
               upx = True,
               name = 'Lyrics')

# Bundle application on macOS
if platform.system() == 'Darwin':
    app = BUNDLE(exe,
                 name = 'Lyrics.app',
                 bundle_identifier = None,
                 info_plist = {
                    'NSHighResolutionCapable': 'True'
                 })
