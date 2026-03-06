"""
scraper.py — Scrapling を使ったスクレイピングサンプル

【インストール】
    pip install "scrapling[fetchers]"
    scrapling install
"""

import asyncio
import sys


# ──────────────────────────────────────────────
# 設定
# ──────────────────────────────────────────────

# スクレイピング先 URL
TARGET_URL = "https://quotes.toscrape.com/"


# ──────────────────────────────────────────────
# 1. 軽量パーサー（ネットワーク接続なし）
# ──────────────────────────────────────────────

def parse_html():
    """手元の HTML 文字列をそのままパースする"""
    from scrapling.parser import Selector

    html = """
    <ul>
      <li class="item"><h2>商品A</h2><span class="price">¥1,000</span></li>
      <li class="item"><h2>商品B</h2><span class="price">¥2,500</span></li>
    </ul>
    """
    page = Selector(html)
    for item in page.css('.item'):
        print(f"  {item.css('h2::text').get()}  {item.css('.price::text').get()}")


# ──────────────────────────────────────────────
# 2. 通常の HTTP リクエスト
# ──────────────────────────────────────────────

def fetch_http():
    """通常サイト向け。ブラウザの TLS フィンガープリントを模倣"""
    from scrapling.fetchers import Fetcher

    page = Fetcher.get(TARGET_URL, stealthy_headers=True)
    for quote in page.css('.quote')[:3]:
        text   = quote.css('.text::text').get()
        author = quote.css('.author::text').get()
        print(f"  [{author}] {text[:50]}...")


# ──────────────────────────────────────────────
# 3. ブラウザ自動化（JavaScript が必要なサイト向け）
# ──────────────────────────────────────────────

def fetch_browser():
    """JavaScript を実行するサイトはこちら"""
    from scrapling.fetchers import DynamicFetcher

    page = DynamicFetcher.fetch(TARGET_URL, headless=True, network_idle=True)
    quotes = page.css('.quote .text::text').getall()
    print(f"  取得件数: {len(quotes)} 件")
    for q in quotes[:3]:
        print(f"  {q[:60]}...")


# ──────────────────────────────────────────────
# 4. ステルス（Cloudflare など強力な Bot 対策のあるサイト向け）
# ──────────────────────────────────────────────

def fetch_stealth():
    """Cloudflare Turnstile を自動突破する高ステルスモード"""
    from scrapling.fetchers import StealthyFetcher

    page = StealthyFetcher.fetch(
        "https://nopecha.com/demo/cloudflare",
        headless=True,
        solve_cloudflare=True,
    )
    links = page.css('#padded_content a::text').getall()
    print(f"  取得リンク数: {len(links)} 件")


# ──────────────────────────────────────────────
# 5. 非同期並列リクエスト
# ──────────────────────────────────────────────

async def _fetch_pages_async():
    from scrapling.fetchers import AsyncFetcher

    urls = [f"{TARGET_URL}page/{i}/" for i in range(1, 4)]
    pages = await asyncio.gather(*[AsyncFetcher.get(u) for u in urls])
    for i, page in enumerate(pages, 1):
        print(f"  ページ{i}: {len(page.css('.quote'))} 件")

def fetch_async():
    """複数ページを同時に取得して速度アップ"""
    asyncio.run(_fetch_pages_async())


# ──────────────────────────────────────────────
# 6. クローラー（複数ページを自動で辿る）
# ──────────────────────────────────────────────

def crawl():
    """次ページリンクを自動で追いかけて全件取得 → JSON 保存"""
    from scrapling.spiders import Spider, Response

    class QuotesSpider(Spider):
        name = "quotes"
        start_urls = [TARGET_URL]
        concurrent_requests = 5

        async def parse(self, response: Response):
            for quote in response.css('.quote'):
                yield {
                    "text": quote.css('.text::text').get(),
                    "author": quote.css('.author::text').get(),
                    "tags": quote.css('.tags .tag::text').getall(),
                }
            # 次ページがあれば続ける
            next_btn = response.css('.next a')
            if next_btn:
                yield response.follow(next_btn[0].attrib['href'])

    result = QuotesSpider().start()
    result.items.to_json("quotes.json")
    print(f"  合計 {len(result.items)} 件 → quotes.json に保存")


# ──────────────────────────────────────────────
# 7. アダプティブ（サイト改修後も要素を再発見）
# ──────────────────────────────────────────────

def fetch_adaptive():
    """
    auto_save=True で要素の特徴を DB に記憶。
    サイトの構造が変わっても adaptive=True で自動再発見する。
    """
    from scrapling.fetchers import Fetcher

    page = Fetcher.get(TARGET_URL)
    quotes = page.css('.quote', auto_save=True)
    print(f"  通常取得:      {len(quotes)} 件 (DB に保存)")

    quotes_ad = page.css('.quote', adaptive=True)
    print(f"  アダプティブ:  {len(quotes_ad)} 件")


# ──────────────────────────────────────────────
# メニュー
# ──────────────────────────────────────────────

MODES = {
    "1": ("パーサーのみ（ネット不要）", parse_html),
    "2": ("通常 HTTP リクエスト", fetch_http),
    "3": ("ブラウザ自動化（JS 対応）", fetch_browser),
    "4": ("ステルス（Cloudflare 回避）", fetch_stealth),
    "5": ("非同期並列リクエスト", fetch_async),
    "6": ("クローラー（全ページ → JSON）", crawl),
    "7": ("アダプティブ（サイト変更に自動追従）", fetch_adaptive),
}

def main():
    # コマンドライン引数で直接指定も可能: python scraper.py 2
    if len(sys.argv) > 1 and sys.argv[1] in MODES:
        choice = sys.argv[1]
    else:
        print("\n  ┌─────────────────────────────────────────┐")
        print("  │      Scrapling スクレイピングサンプル     │")
        print("  └─────────────────────────────────────────┘")
        for k, (desc, _) in MODES.items():
            print(f"    {k}.  {desc}")
        print("    0.  全モードを順番に実行")
        print()
        choice = input("  番号を入力 → ").strip()

    targets = list(MODES.values()) if choice == "0" else (
        [MODES[choice]] if choice in MODES else []
    )
    if not targets:
        print("  無効な番号です。")
        return

    for desc, fn in targets:
        print(f"\n▶ {desc}")
        print("  " + "─" * 40)
        try:
            fn()
        except ImportError:
            print("  フェッチャーが未インストールです")
            print("  👉 pip install 'scrapling[fetchers]' && scrapling install")
        except Exception as e:
            print(f"  ✗ エラー: {e}")

    print("\n  完了！")

if __name__ == "__main__":
    main()