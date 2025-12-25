#!/usr/bin/env python3
"""
書籍に関する感想・批評が含まれるかを人間が確認して振り分けるアプリケーション

操作方法:
  1 : hugo-blog/content/posts に移動（公開）
  0 : hugo-blog-content-nonpublish/ に移動（非公開）
  s : スキップ（後で確認）
  q : 終了
"""

import os
import shutil
from pathlib import Path


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_pending_posts(source_dir: Path) -> list[Path]:
    """処理待ちの投稿フォルダを取得"""
    if not source_dir.exists():
        return []

    folders = sorted([
        d for d in source_dir.iterdir()
        if d.is_dir() and (d / 'index.md').exists()
    ])
    return folders


def display_post(post_dir: Path) -> str:
    """投稿内容を表示"""
    index_file = post_dir / 'index.md'
    if not index_file.exists():
        return "(ファイルが見つかりません)"

    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    return content


def move_post(post_dir: Path, dest_dir: Path):
    """投稿フォルダを移動"""
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / post_dir.name

    if dest_path.exists():
        shutil.rmtree(dest_path)

    shutil.move(str(post_dir), str(dest_path))
    return dest_path


def main():
    base_dir = Path(__file__).parent
    source_dir = base_dir / 'hugo-blog-content-suspicious-candidate'
    publish_dir = base_dir / 'hugo-blog' / 'content' / 'posts'
    nonpublish_dir = base_dir / 'hugo-blog-content-nonpublish'

    print("=" * 60)
    print("書籍感想・批評 振り分けツール")
    print("=" * 60)
    print()
    print("操作方法:")
    print("  1 : hugo-blog/content/posts に移動（公開）")
    print("  0 : hugo-blog-content-nonpublish/ に移動（非公開）")
    print("  s : スキップ（後で確認）")
    print("  q : 終了")
    print()

    posts = get_pending_posts(source_dir)

    if not posts:
        print("処理する投稿がありません。")
        return

    print(f"処理待ち: {len(posts)} 件")
    print()
    input("Enterキーを押して開始...")

    processed = 0
    published = 0
    nonpublished = 0
    skipped = 0

    i = 0
    while i < len(posts):
        post = posts[i]
        clear_screen()

        remaining = len(posts) - i
        print("=" * 60)
        print(f"[{i + 1}/{len(posts)}] 残り: {remaining} 件")
        print(f"フォルダ: {post.name}")
        print("=" * 60)
        print()

        content = display_post(post)
        print(content)

        print()
        print("-" * 60)
        print("1=公開 | 0=非公開 | s=スキップ | q=終了")
        print("-" * 60)

        while True:
            choice = input("選択: ").strip().lower()

            if choice == '1':
                dest = move_post(post, publish_dir)
                print(f"→ 公開: {dest}")
                published += 1
                processed += 1
                posts.pop(i)
                break
            elif choice == '0':
                dest = move_post(post, nonpublish_dir)
                print(f"→ 非公開: {dest}")
                nonpublished += 1
                processed += 1
                posts.pop(i)
                break
            elif choice == 's':
                print("→ スキップ")
                skipped += 1
                i += 1
                break
            elif choice == 'q':
                print()
                print("=" * 60)
                print("終了")
                print(f"  処理済み: {processed} 件")
                print(f"    公開: {published} 件")
                print(f"    非公開: {nonpublished} 件")
                print(f"  スキップ: {skipped} 件")
                print(f"  未処理: {len(posts)} 件")
                print("=" * 60)
                return
            else:
                print("1, 0, s, q のいずれかを入力してください")

    print()
    print("=" * 60)
    print("全件処理完了")
    print(f"  公開: {published} 件")
    print(f"  非公開: {nonpublished} 件")
    print(f"  スキップ: {skipped} 件")
    print("=" * 60)


if __name__ == '__main__':
    main()
