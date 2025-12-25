your_facebooc_activity フォルダは FaceBook の個人データを JSON 形式でエクスポートしたもののうち
post フォルダに含まれるデータです。

このフォルダにある Facebook の投稿データに対し

- アクセス範囲が「公開」になっているものを抽出
- MarkDown 形式に変換
- Hugo のブログ記事として出力
- MarkDown ファイル,  画像ファイル, GitHub Pages として公開する GitHub Actions を 専用の GitHub リポジトリとして作成
- your_facebooc_activity は GitHub リポジトリに含めない (.gitignore に追加)
