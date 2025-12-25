#!/usr/bin/env python3
"""
Facebook JSON データを Hugo ブログ記事に変換するスクリプト
"""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path
import re


def decode_facebook_text(text: str) -> str:
    """Facebook JSON のエスケープされた UTF-8 を正しくデコード"""
    if not text:
        return ""
    try:
        # Facebook は Latin-1 としてエンコードされた UTF-8 バイトを出力する
        return text.encode('latin-1').decode('utf-8')
    except (UnicodeDecodeError, UnicodeEncodeError):
        return text


def sanitize_filename(text: str) -> str:
    """ファイル名として使える文字列に変換"""
    # 改行とタブを空白に
    text = re.sub(r'[\n\r\t]+', ' ', text)
    # ファイル名に使えない文字を除去
    text = re.sub(r'[<>:"/\\|?*]', '', text)
    # 連続する空白を1つに
    text = re.sub(r'\s+', ' ', text)
    # 前後の空白を除去し、長さを制限
    return text.strip()[:50]


def convert_timestamp(ts: int) -> tuple[str, str]:
    """Unix タイムスタンプを日付文字列に変換"""
    dt = datetime.fromtimestamp(ts)
    return dt.strftime('%Y-%m-%d'), dt.strftime('%Y-%m-%dT%H:%M:%S+09:00')


def extract_post_content(post: dict) -> str:
    """投稿からテキストコンテンツを抽出"""
    content = ""
    if 'data' in post:
        for data in post['data']:
            if isinstance(data, dict) and 'post' in data:
                content = decode_facebook_text(data['post'])
                break
    return content


def extract_attachments(post: dict) -> list[dict]:
    """投稿から添付ファイル情報を抽出"""
    attachments = []
    if 'attachments' not in post:
        return attachments

    for att in post['attachments']:
        if 'data' not in att:
            continue
        for data in att['data']:
            if 'media' in data:
                media = data['media']
                attachments.append({
                    'type': 'media',
                    'uri': media.get('uri', ''),
                    'description': decode_facebook_text(media.get('description', '')),
                    'title': decode_facebook_text(media.get('title', ''))
                })
            elif 'external_context' in data:
                ext = data['external_context']
                attachments.append({
                    'type': 'link',
                    'url': ext.get('url', ''),
                    'name': decode_facebook_text(ext.get('name', ''))
                })
            elif 'place' in data:
                place = data['place']
                attachments.append({
                    'type': 'place',
                    'name': decode_facebook_text(place.get('name', '')),
                    'address': decode_facebook_text(place.get('address', ''))
                })
    return attachments


def generate_hugo_frontmatter(date_iso: str, title: str, tags: list[str] = None) -> str:
    """Hugo のフロントマターを生成"""
    tags = tags or []
    frontmatter = f'''---
title: "{title}"
date: {date_iso}
draft: false
'''
    if tags:
        frontmatter += f"tags: {tags}\n"
    frontmatter += "---\n\n"
    return frontmatter


def generate_hugo_content(post: dict, media_dest_dir: Path, source_base: Path) -> tuple[str, str, list[str]]:
    """Hugo 記事のコンテンツを生成"""
    content = extract_post_content(post)
    attachments = extract_attachments(post)

    # 画像ファイルのリスト（コピー対象）
    media_files = []

    # 添付ファイルをマークダウンに変換
    attachment_md = ""
    for att in attachments:
        if att['type'] == 'media' and att['uri']:
            uri = att['uri']
            # メディアファイルのパスを取得
            media_path = source_base / uri
            if media_path.exists():
                filename = os.path.basename(uri)
                media_files.append((str(media_path), filename))
                attachment_md += f"\n![{att.get('description', '')}]({filename})\n"
        elif att['type'] == 'link' and att['url']:
            link_text = att.get('name') or att['url']
            attachment_md += f"\n[{link_text}]({att['url']})\n"
        elif att['type'] == 'place' and att['name']:
            place_info = att['name']
            if att.get('address'):
                place_info += f" ({att['address']})"
            attachment_md += f"\n📍 {place_info}\n"

    # タイトルを生成
    title = content[:100] if content else "Facebook投稿"
    title = sanitize_filename(title)
    if not title:
        title = "Facebook投稿"

    full_content = content + attachment_md

    return full_content, title, media_files


def load_facebook_posts(json_path: Path) -> list[dict]:
    """Facebook の投稿 JSON を読み込む"""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def convert_posts_to_hugo(
    input_json: Path,
    output_dir: Path,
    source_base: Path,
    max_posts: int = None
):
    """Facebook 投稿を Hugo 記事に変換"""
    posts = load_facebook_posts(input_json)

    # 出力ディレクトリを作成
    content_dir = output_dir / 'content' / 'posts'
    static_dir = output_dir / 'static' / 'images'
    content_dir.mkdir(parents=True, exist_ok=True)
    static_dir.mkdir(parents=True, exist_ok=True)

    converted_count = 0

    for i, post in enumerate(posts):
        if max_posts and i >= max_posts:
            break

        if 'timestamp' not in post:
            continue

        date_str, date_iso = convert_timestamp(post['timestamp'])

        # 投稿コンテンツを取得
        content, title, media_files = generate_hugo_content(post, static_dir, source_base)

        # コンテンツがない投稿はスキップ（オプション）
        if not content.strip() and not media_files:
            continue

        # ファイル名を生成
        slug = sanitize_filename(title)[:30] if title else str(post['timestamp'])
        slug = re.sub(r'[^\w\-]', '-', slug)
        slug = re.sub(r'-+', '-', slug).strip('-')
        filename = f"{date_str}-{slug or post['timestamp']}.md"

        # 記事用のディレクトリを作成（Page Bundle形式）
        post_dir = content_dir / f"{date_str}-{slug or post['timestamp']}"
        post_dir.mkdir(parents=True, exist_ok=True)

        # 画像をコピー
        for src_path, dest_filename in media_files:
            dest_path = post_dir / dest_filename
            if os.path.exists(src_path) and not dest_path.exists():
                shutil.copy2(src_path, dest_path)

        # 記事を書き出し
        frontmatter = generate_hugo_frontmatter(date_iso, title)
        article_path = post_dir / 'index.md'
        with open(article_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter)
            f.write(content)

        converted_count += 1
        if converted_count % 100 == 0:
            print(f"  {converted_count} 件変換完了...")

    return converted_count


def main():
    """メイン処理"""
    # パスの設定
    base_dir = Path(__file__).parent
    source_base = base_dir / 'your_facebook_activity'
    input_json = source_base / 'posts' / 'your_posts__check_ins__photos_and_videos_1.json'
    output_dir = base_dir / 'hugo-blog'

    print("Facebook データを Hugo ブログ記事に変換します...")
    print(f"入力: {input_json}")
    print(f"出力: {output_dir}")

    if not input_json.exists():
        print(f"エラー: 入力ファイルが見つかりません: {input_json}")
        return 1

    # 変換を実行
    count = convert_posts_to_hugo(input_json, output_dir, source_base)

    print(f"\n完了! {count} 件の投稿を変換しました。")
    print(f"出力先: {output_dir}")

    return 0


if __name__ == '__main__':
    exit(main())
