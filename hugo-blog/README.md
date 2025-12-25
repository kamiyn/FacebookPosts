# Facebook Archive Blog

Facebook の投稿データを Hugo ブログとして公開するためのリポジトリです。

## セットアップ

### 1. テーマのインストール

```bash
git submodule add https://github.com/theNewDynamic/gohugo-theme-ananke.git themes/ananke
```

### 2. ローカルプレビュー

```bash
hugo server -D
```

ブラウザで http://localhost:1313 を開く

### 3. GitHub Pages へのデプロイ

1. このリポジトリを GitHub にプッシュ
2. Settings > Pages で Source を "GitHub Actions" に設定
3. main ブランチにプッシュすると自動的にデプロイされます

## ファイル構成

```
hugo-blog/
├── .github/workflows/deploy.yml  # GitHub Actions 設定
├── content/posts/                # 変換された投稿
├── hugo.toml                     # Hugo 設定
└── themes/ananke/                # テーマ
```

## 設定のカスタマイズ

`hugo.toml` で以下を変更してください:

- `baseURL`: あなたの GitHub Pages URL
- `title`: ブログのタイトル
- `[params]`: 著者名、説明文など
