# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['test_clone.py'],
             pathex=[],
             binaries=[],
             datas=[
             ('E:/Python/pyqt5/qrc_rc.py','.'),
             ('E:/Python/pyqt5/CIGIN','CIGIN/'),
             ('E:/Python/pyqt5/tox_21','tox_21/'),
             ('E:/Python/Anaconda3_5.2.0/envs/exe/Lib/site-packages/dgl','dgl/'),
             ('E:/Python/pyqt5/title.png','.'),
             ],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
for d in a.datas:
	if '_C.cp36-win_amd64.pyd' in d[0]:
		a.datas.remove(d)
		break
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='分子探长',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
          icon='D:/火狐/title.ico')
