# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('/Users/neo/Documents/10ML/directory_traversing/src/dart/models.py', 'dart'), ('/Users/neo/Documents/10ML/directory_traversing/src/gui_interface/banner.png', 'gui_interface')],
    hiddenimports=['timm.models.layers.attention_pool2d'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='DART interface 1_1_3',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='DART interface 1_1_3',
)
app = BUNDLE(
    coll,
    name='DART interface 1_1_3.app',
    icon=None,
    bundle_identifier=None,
)
