# pythonコードのデバッグ方法

pip installのdevelopモードを利用する事でpythonファイルの修正が即座に反映され毎回whlファイル生成、pip installが不要となる。

## develop mode
`pyjds/python/src/`フォルダで以下実行する  
`pyjds/python/src$pip install -e .`

`pip list`で以下のように表示されればOK  
```
Package      Version Location
------------ ------- -------------------------------------------------
atomicwrites 1.4.0
attrs        21.4.0
colorama     0.4.4
iniconfig    1.1.1
numpy        1.22.0
packaging    21.3
Pillow       9.0.1
pip          21.1.1
pluggy       1.0.0
py           1.11.0
pyjds        0.0.3   c:\users\nma\work\10.development\pyjds\python\src
pyparsing    3.0.6
pytest       6.2.5
setuptools   56.0.0
toml         0.10.2
```
### pydファイル配置
c++コードから生成されたpydファイルが`pyjds/python/src/pyjds`に存在する必要がある。pydファイルはデバッグ、ビルドの度に`pyjds/python/src/pyjds`以下にコピーが必要である。
pydをコピーする場合はpythonを一旦抜け再度pythonに入りなおす必要がある。  
`import pyjds`を実行しDevelop mode!!!と表示された場合は正しくdevelop modeとして利用できる。
```
(.venv) PS C:\Users\nma\work\10.development\pyJds\python\src> python
Python 3.8.10 (tags/v3.8.10:3d8993a, May  3 2021, 11:48:03) [MSC v.1928 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import pyjds


*************************************************************
Develop mode!!!!!  pyjds path:C:\Users\nma\work\10.development\pyJds\python\src\pyjds
*************************************************************
```

異常な場合は以下のようなエラー表示になる。
```
(.venv) PS C:\Users\nma\work\10.development\pyJds\python\src> python
Python 3.8.10 (tags/v3.8.10:3d8993a, May  3 2021, 11:48:03) [MSC v.1928 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import pyjds


*************************************************************
Develop mode!!!!!  pyjds path:C:\Users\nma\work\10.development\pyJds\python\src\pyjds
*************************************************************
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "C:\Users\nma\work\10.development\pyJds\python\src\pyjds\__init__.py", line 34, in <module>
    from .device_gev import *
  File "C:\Users\nma\work\10.development\pyJds\python\src\pyjds\device_gev.py", line 7, in <module>
    import _module
ModuleNotFoundError: No module named '_module'
>>>
```

## Test
`pyjds/python/test`以下にpytestを使ったテストコードが存在する。develop modeでtest実行する場合は`pyjds/python/src/`フォルダで実行する必要がある。

* 全test実行  
`pyjds/python/src$pytest ../test`

* test_acqusition.py実行  
`pyjds/python/src$pytest ../test/test_acqusition.py`

* test_acqusition.pyのtest_acquisitionを実行  
`pyjds/python/src$pytest ..\test\test_acqusition.py::Test::test_acquisition`

