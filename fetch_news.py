from massive import RESTClient
import os

API_KEY = os.environ.get("MASSIVE_API_KEY", "YOUR_KEY_HERE")
client = RESTClient(api_key=API_KEY)

news_items = []
for article in client.list_ticker_news(
    ticker="AAPL",
    published_utc_gte="2024-01-01T00:00:00Z",
    published_utc_lte="2026-09-26T23:59:59Z",
    limit=1000,
    order="asc"
):
    news_items.append({
        "title": article.title,
        "published": article.published_utc,
        "description": article.description
    })

print(f"Total news fetched: {len(news_items)}")
