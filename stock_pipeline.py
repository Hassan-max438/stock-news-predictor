# pyright: reportMissingImports=false

from massive import RESTClient
import pandas as pd
import time
from datetime import datetime, timedelta

# ============================================
# 🔑 STEP 0: API KEY
# ============================================
API_KEY = "s5T4n30QAYOXp7q9Qg8047uuy9wmgH3o"
client = RESTClient(api_key=API_KEY)

# ============================================
# ⚙️ SETTINGS
# ============================================
TICKER = "AAPL"
START_DATE = "2026-03-26"
END_DATE = "2026-09-26"

SPIKE_THRESHOLD = 0.001
DECLINE_THRESHOLD = -0.001

# ============================================
# 📰 STEP 1: FETCH NEWS (mahine-mahine)
# ============================================
print("=" * 50)
print("STEP 1: Fetching news (month by month)...")
print("=" * 50)

news_items = []
start = datetime.strptime(START_DATE, "%Y-%m-%d")
end = datetime.strptime(END_DATE, "%Y-%m-%d")
current = start

while current < end:
    next_month = (current.replace(day=1) + timedelta(days=32)).replace(day=1)
    if next_month > end:
        next_month = end

    from_str = current.strftime("%Y-%m-%dT00:00:00Z")
    to_str = next_month.strftime("%Y-%m-%dT23:59:59Z")

    print(f"  → {current.strftime('%b %Y')}...")

    try:
        for article in client.list_ticker_news(
            ticker=TICKER,
            published_utc_gte=from_str,
            published_utc_lte=to_str,
            limit=1000,
            order="asc"
        ):
            news_items.append({
                "title": article.title,
                "published": article.published_utc,
                "description": article.description
            })
    except Exception as e:
        print(f"    ⚠️ Error: {e}, skipping month")

    current = next_month
    time.sleep(15)

df_news = pd.DataFrame(news_items)
df_news.to_csv("stock_news.csv", index=False)
print(f"✅ Total news: {len(df_news)}")

# ============================================
# 📈 STEP 2: FETCH PRICES (mahine-mahine)
# ============================================
print("\n" + "=" * 50)
print("STEP 2: Fetching 5-min bars (month by month)...")
print("=" * 50)

price_bars = []
current = start

while current < end:
    next_month = (current.replace(day=1) + timedelta(days=32)).replace(day=1)
    if next_month > end:
        next_month = end

    from_str = current.strftime("%Y-%m-%d")
    to_str = next_month.strftime("%Y-%m-%d")

    print(f"  → {current.strftime('%b %Y')}...")

    try:
        for bar in client.list_aggs(
            ticker=TICKER,
            multiplier=5,
            timespan="minute",
            from_=from_str,
            to=to_str,
            limit=50000
        ):
            price_bars.append({
                "time": bar.timestamp,
                "open": bar.open,
                "high": bar.high,
                "low": bar.low,
                "close": bar.close,
                "volume": bar.volume
            })
    except Exception as e:
        print(f"    ⚠️ Error: {e}, skipping month")

    current = next_month
    time.sleep(15)

df_prices = pd.DataFrame(price_bars)
df_prices.to_csv("stock_prices_5min.csv", index=False)
print(f"✅ Total bars: {len(df_prices)}")

# ============================================
# 🏷️ STEP 3: LABEL
# ============================================
print("\n" + "=" * 50)
print("STEP 3: Labeling...")
print("=" * 50)

if df_news.empty or df_prices.empty:
    print("❌ Data empty — cannot label")
else:
    df_news["published"] = pd.to_datetime(df_news["published"]).dt.tz_localize(None)
    df_prices["time"] = pd.to_datetime(df_prices["time"], unit="ms").dt.tz_localize(None)

    labeled = []
    for _, row in df_news.iterrows():
        closest = df_prices.iloc[
            (df_prices["time"] - row["published"]).abs().argmin()
        ]
        ret = (closest["close"] - closest["open"]) / closest["open"]

        if ret > SPIKE_THRESHOLD:
            label = "spike"
        elif ret < DECLINE_THRESHOLD:
            label = "decline"
        else:
            label = "neutral"

        labeled.append({
            "title": row["title"],
            "published": row["published"],
            "description": row["description"],
            "return": round(ret, 6),
            "label": label
        })

    df_labeled = pd.DataFrame(labeled)
    df_labeled.to_csv("stock_news_labeled.csv", index=False)

    print("\n" + "=" * 50)
    print("📊 FINAL SUMMARY")
    print("=" * 50)
    print(f"Ticker: {TICKER}")
    print(f"Date range: {START_DATE} → {END_DATE}")
    print(f"Total news: {len(df_labeled)}")
    print(f"\nLabel distribution:")
    print(df_labeled["label"].value_counts())
    print(f"\n📁 Files saved:")
    print(f"   - stock_news.csv")
    print(f"   - stock_prices_5min.csv")
    print(f"   - stock_news_labeled.csv")
    print("=" * 50)