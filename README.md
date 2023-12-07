# icon resize for twitch
画像を twitch のチャンネルポイントや、バッジの作成時向けにリサイズするツールです。

# 使い方
Release から最新バージョンの icon-resize-for-twitch.exe をダウンロードします。

exe ファイルを開き、 Open Fileを押して、リサイズするファイルを選択し、リサイズボタンを押すことでリサイズされます。リサイズされたファイルは、元のファイルと同じ場所に作られます。

> [!TIP]
> 事前に正方形にしておくとキレイにリサイズされやすいです。
> アンチエイリアスによってボケてしまう場合は、 No_AA のボタンを使ってください（ファイルは上書きです）

build command

```
pyinstaller .\main.py --name icon-resize-for-twitch.exe --onefile --noconsole
```