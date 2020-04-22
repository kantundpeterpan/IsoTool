# -*- mode: python ; coding: utf-8 -*-

import gooey
gooey_root = os.path.dirname(gooey.__file__)
gooey_languages = Tree(os.path.join(gooey_root, 'languages'), prefix = 'gooey/languages')
gooey_images = Tree(os.path.join(gooey_root, 'images'), prefix = 'gooey/images')

block_cipher = None


a = Analysis(['../isotool.py'],
             pathex=[],
             binaries=[],
             datas=[('../icon/*', 'icon'),('../data/isotopes_terrestrial.csv', 'data')],
             hiddenimports=[],
             hookspath=['./hooks'],
             runtime_hooks=[],
             excludes=['matplotlib', 'PyQt5', 'jupyter', 'IPython', 'nbconvert', 'jedi'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='isotool_linux_onexe',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
