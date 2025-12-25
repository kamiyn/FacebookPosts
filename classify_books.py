#!/usr/bin/env python3
"""
書籍に関する感想・批評で投稿を振り分けるスクリプト
"""

import os
import re
import shutil
from pathlib import Path


# 書籍関連の確実なキーワード（これらが含まれれば書籍関連と判定）
DEFINITE_BOOK_PATTERNS = [
    r'読了',
    r'読み終[わえ]',
    r'読み終わった',
    r'読破',
    r'本を読[んむ]',
    r'読書',
    r'書評',
    r'レビュー.{0,10}(本|書籍|小説|漫画|マンガ)',
    r'(本|書籍|小説|漫画|マンガ).{0,10}レビュー',
    r'(本|書籍|小説|漫画|マンガ).{0,10}感想',
    r'感想.{0,10}(本|書籍|小説|漫画|マンガ)',
    r'(著者|作者|著).{0,5}[「『]',
    r'[「『].{1,30}[」』].{0,10}(を|が|は).{0,5}(読|面白|良|おもしろ)',
    r'(新刊|文庫|単行本|ハードカバー|電子書籍|kindle|Kindle)',
    r'(出版|発売).{0,10}(本|書籍)',
    r'(本|書籍).{0,10}(出版|発売)',
    r'(買った|購入).{0,10}(本|書籍|小説|漫画)',
    r'(本|書籍|小説|漫画).{0,10}(買った|購入)',
    r'図書館.{0,10}(借|返)',
    r'積読',
    r'積ん読',
    r'本棚',
    r'(良書|名著|傑作|駄作)',
    r'(この|その|あの)(本|小説|漫画|作品)は',
    r'(おすすめ|オススメ|お勧め).{0,10}(本|書籍|小説)',
]

# 書籍関連の可能性があるキーワード（疑わしい）
SUSPICIOUS_BOOK_PATTERNS = [
    r'[「『][^」』]{2,50}[」』]',  # 書籍タイトルっぽい括弧
    r'(読んだ|読んでる|読んでいる|読み中)',
    r'(本|書籍)',
    r'(小説|漫画|マンガ|コミック)',
    r'(著者|作者|作家)',
    r'(物語|ストーリー)',
    r'(出版社|講談社|新潮|角川|文春|集英社|岩波|光文社)',
    r'(面白い|面白かった|おもしろ)',
    r'(上巻|下巻|第\d+巻|\d+巻)',
    r'(シリーズ|続編|完結)',
    r'(主人公|登場人物|キャラクター)',
    r'ISBN',
    r'(本屋|書店|紀伊國屋|ジュンク堂|丸善|TSUTAYA)',
    r'(Amazonで|楽天ブックス)',
    r'(ベストセラー|話題の)',
]

# 書籍と関係ない文脈で使われるキーワード（除外パターン）
EXCLUDE_PATTERNS = [
    r'(本日|本当|本人|本物|本来|本気|本格|本番|本社|本部|本店|基本|根本|日本)',
    r'(本の少し|本の一部)',
    r'(絵本|写真集|図鑑|教科書|参考書|問題集)',  # 感想・批評対象外
    r'(技術書|専門書|ビジネス書)',  # 技術系は除外（オプション）
]


def read_post_content(post_dir: Path) -> str:
    """投稿ディレクトリからコンテンツを読み取る"""
    index_path = post_dir / 'index.md'
    if not index_path.exists():
        return ""

    with open(index_path, 'r', encoding='utf-8') as f:
        return f.read()


def classify_post(content: str) -> str:
    """
    投稿を分類する
    Returns: 'definite', 'suspicious', 'nonpublish'
    """
    # 確実な書籍パターンをチェック
    for pattern in DEFINITE_BOOK_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            return 'definite'

    # 疑わしいパターンのカウント
    suspicious_count = 0
    for pattern in SUSPICIOUS_BOOK_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            suspicious_count += 1

    # 除外パターンのカウント（書籍と関係ない「本」の使用など）
    exclude_count = 0
    for pattern in EXCLUDE_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            exclude_count += 1

    # 疑わしいパターンが2つ以上あり、除外パターンより多ければ suspicious
    if suspicious_count >= 2 and suspicious_count > exclude_count:
        return 'suspicious'

    return 'nonpublish'


def main():
    base_dir = Path('/mnt/g/temp/facebook-kamiyn-2025_12_25-5XfLtXCH')
    source_dir = base_dir / 'hugo-blog-content-candidate'

    # 出力ディレクトリ（同じ場所を使用）
    definite_dir = base_dir / 'hugo-blog-content-candidate'
    suspicious_dir = base_dir / 'hugo-blog-content-suspicious-candidate'
    nonpublish_dir = base_dir / 'hugo-blog-content-nonpublish'

    # 出力ディレクトリを作成
    suspicious_dir.mkdir(exist_ok=True)
    nonpublish_dir.mkdir(exist_ok=True)

    # 統計
    stats = {'definite': 0, 'suspicious': 0, 'nonpublish': 0}

    # 全投稿を処理
    posts = list(source_dir.iterdir())
    total = len(posts)

    print(f"処理開始: {total} 件の投稿")

    for i, post_dir in enumerate(posts):
        if not post_dir.is_dir():
            continue

        content = read_post_content(post_dir)
        classification = classify_post(content)

        # 移動先を決定
        if classification == 'definite':
            # そのまま残す
            stats['definite'] += 1
        elif classification == 'suspicious':
            dest = suspicious_dir / post_dir.name
            if not dest.exists():
                shutil.move(str(post_dir), str(dest))
            stats['suspicious'] += 1
        else:
            dest = nonpublish_dir / post_dir.name
            if not dest.exists():
                shutil.move(str(post_dir), str(dest))
            stats['nonpublish'] += 1

        if (i + 1) % 500 == 0:
            print(f"  {i + 1}/{total} 件処理完了...")

    print(f"\n完了!")
    print(f"  確実に書籍関連: {stats['definite']} 件 (hugo-blog-content-candidate/)")
    print(f"  可能性あり: {stats['suspicious']} 件 (hugo-blog-content-suspicious-candidate/)")
    print(f"  書籍関連なし: {stats['nonpublish']} 件 (hugo-blog-content-nonpublish/)")


if __name__ == '__main__':
    main()
