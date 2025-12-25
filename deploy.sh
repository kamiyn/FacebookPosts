#!/bin/bash
# Hugo サイトのローカルビルドスクリプト
# .github/workflows/deploy.yml の Build ステージと同等の処理を実行

set -e

HUGO_VERSION="0.128.0"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HUGO_BLOG_DIR="${SCRIPT_DIR}/hugo-blog"

# 色付き出力
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

# Hugo がインストールされているか確認
check_hugo() {
    if command -v hugo &> /dev/null; then
        INSTALLED_VERSION=$(hugo version | grep -oP 'v\K[0-9]+\.[0-9]+\.[0-9]+' | head -1)
        info "Hugo version ${INSTALLED_VERSION} is installed"
        return 0
    else
        warn "Hugo is not installed"
        return 1
    fi
}

# Hugo のインストール (Linux)
install_hugo() {
    info "Installing Hugo ${HUGO_VERSION}..."

    TEMP_DIR=$(mktemp -d)
    HUGO_DEB="${TEMP_DIR}/hugo.deb"

    wget -O "${HUGO_DEB}" "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.deb"
    sudo dpkg -i "${HUGO_DEB}"

    rm -rf "${TEMP_DIR}"

    info "Hugo ${HUGO_VERSION} installed successfully"
}

# サブモジュールの更新
update_submodules() {
    info "Updating git submodules..."
    cd "${SCRIPT_DIR}"
    git submodule update --init --recursive
}

# Node.js 依存関係のインストール
install_node_deps() {
    cd "${HUGO_BLOG_DIR}"

    if [[ -f package-lock.json || -f npm-shrinkwrap.json ]]; then
        info "Installing Node.js dependencies..."
        npm ci
    else
        info "No package-lock.json or npm-shrinkwrap.json found, skipping npm install"
    fi
}

# Hugo でビルド
build_hugo() {
    cd "${HUGO_BLOG_DIR}"

    info "Building Hugo site..."

    export HUGO_ENVIRONMENT=production
    export TZ=Asia/Tokyo

    # baseURL は環境変数で上書き可能
    if [[ -n "${BASE_URL}" ]]; then
        hugo --gc --minify --baseURL "${BASE_URL}"
    else
        hugo --gc --minify
    fi

    info "Build completed successfully!"
    info "Output directory: ${HUGO_BLOG_DIR}/public"
}

# メイン処理
main() {
    info "Starting Hugo build process..."

    # Hugo の確認・インストール
    if ! check_hugo; then
        install_hugo
    fi

    # サブモジュールの更新
    update_submodules

    # Node.js 依存関係のインストール
    install_node_deps

    # Hugo ビルド
    build_hugo

    info "All done!"
}

main "$@"
