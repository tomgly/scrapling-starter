# 🕷️ scrapling-starter

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![Scrapling](https://img.shields.io/badge/Powered%20by-Scrapling-green)](https://github.com/D4Vinci/Scrapling)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

**Scrapling** を使った Web スクレイピングのスターターキットです。  
コピペだけで動くサンプルを7種類用意しています。

## ファイル構成

```
scrapling-starter/
├── scraper.py        # メインスクリプト
├── requirements.txt  # 依存パッケージ
├── .gitignore
└── README.md
```

## クイックスタート（3ステップ）

### 1. リポジトリをクローン

```bash
git clone https://github.com/tomgly/scrapling-starter.git
cd scrapling-starter
```

### 2. インストール

```bash
pip install -r requirements.txt
scrapling install # ブラウザ依存ファイルのダウンロード（数分かかります）
```

### 3. 実行

```bash
python scraper.py
```

メニューが出るので番号を選ぶだけ！

```
  ┌─────────────────────────────────────────┐
  │      Scrapling スクレイピングサンプル     │
  └─────────────────────────────────────────┘
    1.  パーサーのみ（ネット不要）
    2.  通常 HTTP リクエスト
    3.  ブラウザ自動化（JS 対応）
    4.  ステルス（Cloudflare 回避）
    5.  非同期並列リクエスト
    6.  クローラー（全ページ → JSON）
    7.  アダプティブ（サイト変更に自動追従）
    0.  全モードを順番に実行
```

番号はコマンドラインで直接渡すこともできます：

```bash
python scraper.py 2   # 通常 HTTP をすぐ実行
python scraper.py 6   # クローラーをすぐ実行
```

## モード一覧

| # | モード | 向いているサイト |
|---|--------|-----------------|
| 1 | パーサーのみ | 手元の HTML を解析したいとき |
| 2 | 通常 HTTP | 一般的な静的サイト |
| 3 | ブラウザ自動化 | JavaScript が必要なサイト |
| 4 | ステルス | Cloudflare などの強い Bot 対策があるサイト |
| 5 | 非同期並列 | 複数ページを速く取得したいとき |
| 6 | クローラー | 次ページを自動で追って全件取得したいとき |
| 7 | アダプティブ | サイト改修後も壊れずに動かし続けたいとき |

> 初めての人は **1 → 2 → 6** の順に試すのがおすすめです。

## スクレイピング先の変更

`scraper.py` 上部の `TARGET_URL` を書き換えるだけです：

```python
TARGET_URL = "https://quotes.toscrape.com/"  # ← ここを変えるだけ
```

## よくあるエラー

| エラー | 対処 |
|--------|------|
| `No module named 'scrapling'` | `pip install -r requirements.txt` |
| ブラウザが起動しない | `scrapling install --force` |
| `Permission denied`（Mac/Linux） | `pip install --user -r requirements.txt` |
| Windows で文字化け | `chcp 65001` を実行してから `python scraper.py` |

## ライセンス・マナー

- スクレイピング前に対象サイトの `robots.txt` と利用規約を確認してください
- 短時間に大量リクエストを送らないようにしましょう
- 取得データの著作権・個人情報の扱いに注意してください

## 参考リンク

- [Scrapling 公式 GitHub](https://github.com/D4Vinci/Scrapling)
- [Scrapling ドキュメント](https://scrapling.readthedocs.io/en/latest/)
- [練習用サイト（quotes.toscrape.com）](https://quotes.toscrape.com/)