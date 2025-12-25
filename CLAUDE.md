your_facebooc_activity フォルダは FaceBook の個人データを JSON 形式でエクスポートしたもののうち
post フォルダに含まれるデータです。

このフォルダにある Facebook の投稿データに対し

- アクセス範囲が「公開」になっているものを抽出
- MarkDown 形式に変換
- Hugo のブログ記事として出力
- MarkDown ファイル,  画像ファイル, GitHub Pages として公開する GitHub Actions を 専用の GitHub リポジトリとして作成
- your_facebooc_activity は GitHub リポジトリに含めない (.gitignore に追加)


hugo-blog-content-candidate/ フォルダは変換後のPOSTを保持するフォルダです。
公開の判断を保留するため hugo-blog/content/posts ではなく一旦ここに保持します


hugo-blog-content-candidate/ にある Hugo post を 書籍に関する感想・批評 があるかどうかで振り分けてください

- hugo-blog-content-candidate/ : 書籍に関する感想・批評が確実に含まれる
- hugo-blog-content-suspicious-candidate/ : 書籍に関する感想・批評が含まれる可能性がある
- hugo-blog-content-nonpublish/ : 書籍に関する感想・批評が含まれない

hugo-blog-content-suspicious-candidate/ : 書籍に関する感想・批評が含まれる可能性がある
にあるものを人間が内容を確認して
hugo-blog/content/posts に移動するようなアプリケーションを作成

MarkDownファイルを表示し、 1ならば hugo-blog/content/posts に移動 、 0ならば hugo-blog-content-nonpublish/ に移動するようなインターフェースを提供してください
