# release build
## Windows
AWSのリリース向けビルド環境を利用する

### AWS環境への接続
リモートデスクトップを使ってアクセス可能
IPアドレスはインスタンス起動ごとに変わる


NVMe SSD
を使っておりインスタンス起動後にディスク初期化必要

WindowsキーとXのキーを同時に押しディスクの管理から追加する
あるいはPowerShellで初期化
https://www.diskpart.com/jp/articles/powershell-initialize-disk.html


Cドライブ：ビルドツールなど

VS2022 build tools
https://visualstudio.microsoft.com/ja/downloads/

Dドライブ：ビルド対象ソース



cmake -DPYTHON_EXECUTABLE='C:\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python39\\python.exe'

cmake --build . --config Release
->\src\pymodule\Release\_module.cp39-win_amd64.pydが生成される

ディレクトリ内が空ではなく、削除時に確認プロンプトを表示させず、隠しファイル、読み取り専用ファイルを含めて削除する場合
Remove-Item .\build\ -Recurse -Force


