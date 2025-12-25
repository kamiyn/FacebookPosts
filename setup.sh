#!/bin/bash
# Facebook データを Hugo ブログに変換し、GitHub Pages 用にセットアップするスクリプト

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Facebook to Hugo 変換スクリプト ==="
echo ""

# 1. 変換スクリプトを実行
echo "1. Facebook データを Hugo 記事に変換中..."
python3 convert.py
echo ""

# 2. Hugo テーマをセットアップ
echo "2. Hugo テーマをセットアップ中..."
cd hugo-blog
if [ ! -d "themes/ananke" ]; then
    git init 2>/dev/null || true
    git submodule add https://github.com/theNewDynamic/gohugo-theme-ananke.git themes/ananke 2>/dev/null || \
    git clone https://github.com/theNewDynamic/gohugo-theme-ananke.git themes/ananke
fi
cd ..
echo ""

# 3. 完了メッセージ
echo "=== セットアップ完了 ==="
echo ""
echo "次のステップ:"
echo "1. hugo-blog ディレクトリを新しい GitHub リポジトリとして公開"
echo "2. GitHub Settings > Pages で GitHub Actions を選択"
echo "3. push すると自動的にデプロイされます"
echo ""
echo "ローカルでプレビュー:"
echo "  cd hugo-blog && hugo server -D"
