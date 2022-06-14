

# SphinxによるAPIドキュメント生成手順

docstringからSphinxドキュメントを生成する手順  
https://qiita.com/futakuchi0117/items/4d3997c1ca1323259844
を参考にしている

## 準備

準備はsphinxを実行するPCで一度実行すればよい。docstringの修正によるAPIドキュメント改定の場合は[build](https://github.com/jai-rd/pyJds/edit/develop/docs/sphinx.md#build)を行えばよい。

### Sphinxインストール

```
$pip install shpinx
$pip install sphinx_rtd_theme
```

### プロジェクト構成
<pre>
├── CMakeLists.txt
├── python
│   ├── src
│   │   ├── LICENSE
│   │   ├── MANIFEST.in
│   │   ├── Makefile
│   │   ├── README.md
│   │   ├── pyjds
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__
│   │   │   ├── camera.py
│   │   │   ├── image.py
│   │   │   └── stream.py
│   │   ├── requirements.txt
│   │   └── setup.py
│   ├── api-docs
│   └── test
│       └── test_camera.py
├── readme.md
</pre>

#### sphinxプロジェクト作成
プロジェクト設定済みでgitにコミットしてある。以下設定は新規時に一度作成すればよい
<details>
<summary>sphinxプロジェクト設定</summary>
	
pyjds/python/src以下のpyファイルからドキュメントを作成する
	

* sphinx-quickstart

  python配下のapi-docsに生成する

  ```bash
  $ mkdir api-docs
  $ sphinx-quickstart api-docs
  ```

  sphinx-quickstart実行すると以下構成でファイルが生成される

  <pre>
  .
  ├── PythonApplication1
  │   ├── PythonApplication1.py
  │   └── PythonApplication1.pyproj
  ├── api-docs
  │   ├── Makefile
  │   ├── _build
  │   ├── _static
  │   ├── _templates
  │   ├── conf.py
  │   ├── index.rst
  │   └── make.bat
  ├── src
  </pre>

* conf.py編集

  api-docs/conf.pyの以下コメント部分を有効にする

  ```python
  import os
  import sys
  sys.path.insert(0, os.path.abspath('../src'))
  ```

  * 拡張機能設定

    pythonコードのdocstringから作成するためconf.pyのextensionsに以下設定を追加

    ```python
    extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon']
    ```

    `sphinx.ext.autodoc`  はdocstringを自動的に読み込むための拡張機能．

    `sphinx.ext.napoleon` はNumpyスタイルかGoogleスタイルのdocstringをパースするための拡張機能です．

* index.rst編集

  トップページに表示するmoduleをapi-docs/index.rstに追加

  ```reStructuredText
  Welcome to pyjds's documentation!
  =================================
  
  .. toctree::
     :maxdepth: 2
     :caption: Contents:
  
     pyjds
  ```

  
#### theme変更
  defaultテーマは見難いのでsphinx_rtd_themeに変更する

* conf.py修正
	```
	html_theme = "sphinx_rtd_theme"
	```
</details>

#### pythonファイル以外のdocument追加
ここまでの設定でpythonファイルのdocstringからsophixを使ってbuildする事でhtml形式のが自動生成される。  
sphinxはpythonソースコード以外のファイルを使う事も可能である。

<details>
<summaryreStructuredText書式のファイルを追加する手順</summary>
	
#### reStructuredText書式のファイルを追加
sphinxはreStructuredText書式を利用している
ここではtop.rstを以下記載する

* top.rst
```
=====================
セクション(レベル１)
=====================

レベル２
========

レベル３
--------

レベル４
^^^^^^^^
```

* index.rst
topを追加
```
.. toctree::
   :maxdepth: 2
   :caption: Contents:

   top
   pyjds
```

</details>

## build
<pre>
├── CMakeLists.txt
├── python
│   ├── src
│   │   ├── requirements.txt
│   │   └── setup.py
│   ├── api-docs
│   └── test
│       └── test_camera.py
├── readme.md
</pre>

`python`フォルダで作業を行う  
`build/src/pymodule/Release/_module.cp38-win_amd64.pyd`ファイルをpython/srcにコピーする
```
$ sphinx-apidoc -f -o ./api-docs ./src/pyjds
$ sphinx-build ./api-docs/ ./api-docs/_build
```
を実行する事で./api_docs/_build以下に生成される

## 特記事項

https://github.com/jai-rd/pyJds/issues/6
