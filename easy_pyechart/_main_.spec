# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['_main_.py'],
    pathex=['E:\\project\\easy_pyechartpy\\easy_pyechart'],
    binaries=[],
    datas=[('D:\\python_resources\\python\\pyecharts\\dist\\_main_\\pyecharts\datasets', 'pyecharts\\datasets')
	,('D:\\python3\\Lib\\site-packages\\pyecharts\\charts', 'pyecharts\\charts')
	,('D:\\python3\\Lib\\site-packages\\pyecharts\\render', 'pyecharts\\render')
	,('D:\\python3\\Lib\\site-packages\\jinja2', 'jinja2')
	,('E:\\project\\easy_pyechartpy\\assets', 'assets')
	,('E:\\服务器资源配置\\chromedriver','.')
	],
   hiddenimports=[
    'selenium',
    'pandas',
    'numpy',
    # 其他需要的模块
],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='_main_',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='_main_',
)
