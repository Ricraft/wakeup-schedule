# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller 打包配置文件
WakeUp Schedule v2.5.0

使用方法:
    pyinstaller build.spec
"""

import os
import sys
from pathlib import Path

# 项目根目录
project_root = Path(SPECPATH)

a = Analysis(
    ['main.py'],
    pathex=[str(project_root), str(project_root / 'src')],
    binaries=[],
    datas=[
        # 资源文件
        ('resources', 'resources'),
        # 数据目录
        ('data', 'data'),
    ],
    hiddenimports=[
        'PyQt6.QtWebEngineWidgets',
        'PyQt6.QtWebEngineCore',
        'openpyxl',
        'bs4',
        'lxml',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
        'tkinter',
    ],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='WakeUpSchedule',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 关键：不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='resources/icon.ico' if (project_root / 'resources' / 'icon.ico').exists() else None,
)
