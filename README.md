# image resize for twitch
画像を twitch のエモート/チャンネルポイントや、バッジの作成時向けにリサイズするツールです。

# 使い方
Release から最新バージョンの image-resize-for-twitch.exe をダウンロードします。

exe ファイルを開き、 Open Fileを押して、リサイズするファイルを選択し、リサイズボタンを押すことでリサイズされます。リサイズされたファイルは、元のファイルと同じ場所に作られます。

AA(アンチエイリアス)の違いで、変換時のコントラストが変わります。エッジのスムーズさに影響があるので、お好みの方をお使いください。

試験的にアニメーション GIF にも対応しています。バグで透過が正しく行われない場合もあります。

> [!TIP]
> 事前に正方形にしておくとキレイにリサイズされやすいです。
> アンチエイリアスによってボケてしまう場合は、 No_AA のボタンを使ってください（ファイルは上書きです）
> 1:1のアスペクト比以外のが画像は、強制的にアスペクト比を1:1に変換します。

## 320px について
チャンネルトップページのバナー向けの変換です。横幅320になるように、アスペクト比を維持したまま、変換します。

memo: python 
そのうち Rye なり pipenv なりに置き換えても良いかも
```
python -m venv .venv
.\.venv\Scripts\activate
```

memo: build command
```
pyinstaller .\main.py --name image-resize-for-twitch.exe --onefile --noconsole --collect-data tkinterdnd2
```
