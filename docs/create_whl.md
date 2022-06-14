# How to create whl file

## 事前準備
setuptools, wheelをpipでインストールする  
一度実行すれば以後必要ない

## pyd build
build設定はCMakelists.txtに定義しており各種環境用のbuildファイルを生成可能
pydファイルはPythonのMinor Version毎に作成必要である。つまりPython3.8, 3.9に対応するには2回buildする必要がある。対象となるPython VersionはCMake実行時にPYTHON_EXECUTABLEを使って指定する。

### create build configuration
* build for Python3.7  
`$cmake -DPYTHON_EXECUTABLE='C:\\Users\\masam\\AppData\\Local\\Programs\\Python\\Python37\\python.exe' ..`

* build for Python3.8  
`$cmake -DPYTHON_EXECUTABLE='C:\\Users\\masam\\AppData\\Local\\Programs\\Python\\Python38\\python.exe' ..`

### How to build
* build pyd
```
$mkdir build
$cd build
$cmake --build . --config Release --clean-first
```

## pydコピー

pyJds\build\src\pymodule\Release配下のpydファイルをpyJds\python\src\pyjdsにコピーする  


## setup.cfg修正
* Version
pyjds/__init__.pyを変更  
https://github.com/jai-rd/pyJds/blob/5ee8ea811c2bb3b96163d22bd21757dd0d2abcf6/python/src/pyjds/__init__.py#L4

## wheel作成
setup.pyをbdist_wheelオプション付きで実行することでdist配下に生成される  
`$python .\setup.py bdist_wheel --plat-name win_amd64`

* whlファイル命名ルール  
https://qiita.com/kannkyo/items/aca48ed928a433c7ca4c  
https://stackoverflow.com/questions/46915070/wheel-files-what-is-the-meaning-of-none-any-in-protobuf-3-4-0-py2-py3-none-a

