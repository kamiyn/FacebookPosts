#!/usr/bin/env python3
"""
書籍に関する感想・批評が含まれるかを人間が確認して振り分けるアプリケーション

機能:
  - 出版社サイトへのURLが含まれる投稿は自動的に公開フォルダに移動
  - それ以外は手動で確認して振り分け

操作方法:
  1 : hugo-blog/content/posts に移動（公開）
  2 : hugo-blog-content-nonpublish/ に移動（非公開）
  s : スキップ（後で確認）
  q : 終了
"""

import os
import shutil
from pathlib import Path

PUBLISHER_DOMAINS = [
    'www.chikumashobo.co.jp',
    'www.kinokuniya.co.jp',
    'www.shinchosha.co.jp',
    'books.bunshun.jp',
    'www.chuko.co.jp',
    'www.kaitakusha.co.jp',
    'bookclub.kodansha.co.jp',
    'www.shoeisha.co.jp',
    'gihyo.jp',
    'www.diamond.co.jp/book',
    'www.borndigital.co.jp/book',
    'www.kotensinyaku.jp/books',
    'www.msz.co.jp/book',
    'www.shobunsha.co.jp',
    'www.kobunsha.com',
    'www.eastpress.co.jp',
    'www.kashiwashobo.co.jp',
    'www.sbcr.jp',
    'yasakashobo.co.jp',
    'book.mynavi.jp',
    'www.kokusho.co.jp',
    'www.utp.or.jp',
    'www.beret.co.jp',
    'www.iwanami.co.jp',
    'www.h-up.com',
    'www.nakanishiya.co.jp',
    'www.php.co.jp/books',
    'www.heibonsha.co.jp/book',
    'www.oreilly.co.jp',
    'www.lambdanote.com',
    'www.asukashinsha.co.jp',
    'www.e-hon.ne.jp',
    'www.hakuyo-sha.co.jp',
    'www.keio-up.co.jp/np/isbn',
    'www.kawade.co.jp',
    'www.kadokawa.co.jp',
    'filmart.co.jp/books',
    'www.intershift.jp',
    'www.tokuma.jp/book',
    'publications.asahi.com',
    'bungaku-report.com/books',
    'www.hakusuisha.co.jp',
    'www.gentosha.co.jp/book',
    'www.zennoh.or.jp',
    'www.tsukiji-shokan.co.jp',
    'www.kousakusha.co.jp',
    'www.seidosha.co.jp',
    'www.showado-kyoto.jp',
    'www.ctp.co.jp/book',
    'www.keisoshobo.co.jp',
    'www.hanmoto.com',
    'www.harashobo.co.jp',
    'www.igaku-shoin.co.jp',
    'www.yuhikaku.co.jp',
    'books.kenkyusha.co.jp',
    'www.forestpub.co.jp',
    'www.kyoritsu-pub.co.jp',
    'dobunkan.co.jp',
    'www.jikushuppan.co.jp',
    'www.9640.jp',
    'www.kress-jp.com',
    'www.maruzen-publishing.co.jp',
    'pub.hozokan.co.jp',
    'www.tokyo-shoseki.co.jp',
    'www.nhk-book.co.jp',
    'www.seikaisha.co.jp',
    'honto.jp',
    'bungaku-report.com',
    'www.seikyusha.co.jp',
    'www.xknowledge.co.jp',
    'www.gaiajapan.co.jp/books',
    'bookpub.jiji.com',
    'www.minervashobo.co.jp',
    'www.natsume.co.jp',
    'www.tokyo-shoseki.co.jp',
    'books.mdn.co.jp',
    'www.hurstpublishers.com/book',
    'keisobiblio.com',
    'www.maar.com',
    'wp.tufs.ac.jp/tufspress',
    'bookplus.nikkei.com',
    'www.shuwasystem.co.jp',
    'eijipress.co.jp',
    'www.tousuishobou.com',
    'iss.ndl.go.jp',
    'www.seshop.com/product',
    'book.pia.co.jp',
    'www.njg.co.jp/book',
    'ishinsha.com',
    'www.ikaros.jp',
    'www.poplar.co.jp/book',
    'www.toho-shoten.co.jp',
    'str.toyokeizai.net/books',
]


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


def get_post_content(post_dir: Path) -> str:
    """投稿内容を取得"""
    index_file = post_dir / 'index.md'
    if not index_file.exists():
        return ""

    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    return content


def contains_publisher_url(content: str) -> bool:
    """出版社サイトへのURLが含まれているかチェック"""
    for domain in PUBLISHER_DOMAINS:
        if domain in content:
            return True
    return False


def move_post(post_dir: Path, dest_dir: Path):
    """投稿フォルダを移動"""
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / post_dir.name

    if dest_path.exists():
        shutil.rmtree(dest_path)

    shutil.move(str(post_dir), str(dest_path))
    return dest_path


def auto_publish_by_url(posts: list[Path], publish_dir: Path) -> tuple[list[Path], int]:
    """出版社URLを含む投稿を自動で公開フォルダに移動"""
    remaining = []
    auto_published = 0

    for post in posts:
        content = get_post_content(post)
        if contains_publisher_url(content):
            dest = move_post(post, publish_dir)
            print(f"  自動公開: {post.name}")
            auto_published += 1
        else:
            remaining.append(post)

    return remaining, auto_published


def main():
    base_dir = Path(__file__).parent
    source_dir = base_dir / 'hugo-blog-content-suspicious-candidate'
    publish_dir = base_dir / 'hugo-blog' / 'content' / 'posts'
    nonpublish_dir = base_dir / 'hugo-blog-content-nonpublish'

    print("=" * 60)
    print("書籍感想・批評 振り分けツール")
    print("=" * 60)
    print()

    posts = get_pending_posts(source_dir)

    if not posts:
        print("処理する投稿がありません。")
        return

    total_posts = len(posts)
    print(f"処理待ち: {total_posts} 件")
    print()

    print("出版社サイトURLを含む投稿を自動振り分け中...")
    posts, auto_published = auto_publish_by_url(posts, publish_dir)
    print(f"  → 自動公開: {auto_published} 件")
    print()

    if not posts:
        print("全件自動処理完了しました。")
        return

    print(f"手動確認が必要: {len(posts)} 件")
    print()
    print("操作方法:")
    print("  1 : hugo-blog/content/posts に移動（公開）")
    print("  2 : hugo-blog-content-nonpublish/ に移動（非公開）")
    print("  s : スキップ（後で確認）")
    print("  q : 終了")
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

        content = get_post_content(post)
        print(content)

        print()
        print("-" * 60)
        print("1=公開 | 2=非公開 | s=スキップ | q=終了")
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
            elif choice == '2':
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
                print(f"  自動公開: {auto_published} 件")
                print(f"  手動処理: {processed} 件")
                print(f"    公開: {published} 件")
                print(f"    非公開: {nonpublished} 件")
                print(f"  スキップ: {skipped} 件")
                print(f"  未処理: {len(posts)} 件")
                print("=" * 60)
                return
            else:
                print("1, 2, s, q のいずれかを入力してください")

    print()
    print("=" * 60)
    print("全件処理完了")
    print(f"  自動公開: {auto_published} 件")
    print(f"  手動処理: {processed} 件")
    print(f"    公開: {published} 件")
    print(f"    非公開: {nonpublished} 件")
    print(f"  スキップ: {skipped} 件")
    print("=" * 60)


if __name__ == '__main__':
    main()
