import os
import sys
import PyInstaller.__main__
import shutil

# 清理之前的构建
if os.path.exists('dist'):
    shutil.rmtree('dist')
if os.path.exists('build'):
    shutil.rmtree('build')

# 定义应用程序图标
icon_path = 'icon.jpg'

# 定义需要包含的数据文件
datas = [
    ('icon.jpg', '.'),
    ('data', 'data')
]

# 定义需要排除的模块
excludes = [
    'matplotlib', 'scipy', 'PIL', 'PyQt5.QtWebEngineWidgets',
    'PyQt5.QtWebEngine', 'PyQt5.QtWebEngineCore', 'PyQt5.QtMultimedia',
    'PyQt5.QtBluetooth', 'PyQt5.QtWebChannel', 'PyQt5.QtPositioning',
    'PyQt5.QtLocation', 'PyQt5.QtNfc', 'PyQt5.QtQuick', 'PyQt5.QtQuickWidgets',
    'PyQt5.QtSensors', 'PyQt5.QtSerialPort', 'PyQt5.QtSql', 'PyQt5.QtTest',
    'PyQt5.QtXml', 'PyQt5.QtXmlPatterns', 'PyQt5.QtHelp', 'PyQt5.QtPrintSupport',
    'PyQt5.QtSvg', 'PyQt5.QtDesigner', 'PyQt5.QtNetwork', 'PyQt5.QtQml',
    'numpy.random', 'numpy.linalg', 'numpy.fft', 'numpy.lib.tests',
    'pandas.tests', 'pandas.io.formats.style', 'pandas.io.excel._xlsxwriter',
    'pandas.io.excel._openpyxl', 'pandas.io.excel._odswriter', 'pandas.io.excel._pyxlsb',
    'pandas.io.excel._xlwt', 'pandas.io.excel._xlrd', 'pandas.io.formats.excel',
    'pandas.io.formats.printing', 'pandas.io.clipboard', 'pandas.io.parsers.python_parser',
    'pandas.core.window.ewm', 'pandas.core.window.expanding', 'pandas.core.window.rolling',
    'pandas.core.computation', 'pandas.core.reshape.reshape', 'pandas.core.reshape.pivot',
    'pandas.core.reshape.melt', 'pandas.core.reshape.merge', 'pandas.core.reshape.concat',
    'pandas.core.arrays.sparse', 'pandas.core.arrays.interval', 'pandas.core.arrays.categorical',
    'pandas.core.arrays.period', 'pandas.core.arrays.timedeltas', 'pandas.core.arrays.datetimes',
    'pandas.core.dtypes.dtypes', 'pandas.core.dtypes.cast', 'pandas.core.dtypes.missing',
    'pandas.core.dtypes.common', 'pandas.core.dtypes.base', 'pandas.core.dtypes.inference',
    'pandas.core.dtypes.concat', 'pandas.core.dtypes.generic', 'pandas.core.dtypes.missing',
    'pandas.core.dtypes.dtypes', 'pandas.core.dtypes.cast', 'pandas.core.dtypes.base',
    'pandas.core.dtypes.inference', 'pandas.core.dtypes.concat', 'pandas.core.dtypes.generic',
    'pandas.core.dtypes.missing', 'pandas.core.dtypes.dtypes', 'pandas.core.dtypes.cast',
    'pandas.core.dtypes.base', 'pandas.core.dtypes.inference', 'pandas.core.dtypes.concat',
    'pandas.core.dtypes.generic', 'pandas.core.dtypes.missing', 'pandas.core.dtypes.dtypes',
    'pandas.core.dtypes.cast', 'pandas.core.dtypes.base', 'pandas.core.dtypes.inference',
    'pandas.core.dtypes.concat', 'pandas.core.dtypes.generic', 'pandas.core.dtypes.missing',
]

# 定义PyInstaller参数
args = [
    'main.py',                      # 主脚本
    '--name=新乐中医院郭神医专属',   # 应用程序名称
    '--onefile',                    # 打包为单个exe文件
    '--windowed',                   # 使用窗口模式（不显示控制台）
    '--clean',                      # 清理临时文件
    '--noconfirm',                  # 不询问确认
    '--strip',                      # 去除符号表和调试信息
    '--noupx',                      # 不使用UPX压缩
    '--log-level=WARN',             # 减少日志输出
]

# 添加图标
if os.path.exists(icon_path):
    args.append(f'--icon={icon_path}')

# 添加数据文件
for src, dst in datas:
    if os.path.exists(src):
        args.append(f'--add-data={src}{os.pathsep}{dst}')

# 添加排除模块
for module in excludes:
    args.append(f'--exclude-module={module}')

# 添加必要的隐藏导入
args.extend([
    '--hidden-import=pandas._libs.tslibs.timedeltas',
    '--hidden-import=pandas._libs.tslibs.nattype',
    '--hidden-import=pandas._libs.tslibs.np_datetime',
    '--hidden-import=pandas._libs.skiplist',
])

# 运行PyInstaller
PyInstaller.__main__.run(args)

print("打包完成！可执行文件位于 dist 目录中。")