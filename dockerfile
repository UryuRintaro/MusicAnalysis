# ベースイメージ：互換性の高い Python 3.9 (軽量版)
FROM python:3.9-slim

# 必要なシステムライブラリのインストール
# git: GitHubからインストールするため
# ffmpeg, libsndfile1: 音声処理に必須
# build-essential: C++のコンパイルに必要
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    libsndfile1 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリの設定
WORKDIR /app

# Pythonライブラリのインストール
# 1. まずビルドに必要な numpy, cython を入れる
RUN pip install --no-cache-dir numpy scipy cython

# 2. madmom を GitHub の最新版からインストール
# (PyPI版は古いため、GitHub版を使うことでエラーを回避)
RUN pip install --no-cache-dir git+https://github.com/CPJKU/madmom.git

# コンテナ起動時のデフォルトコマンド
CMD ["python3"]