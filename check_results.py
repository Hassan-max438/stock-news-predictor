import pandas as pd

df = pd.read_csv("stock_news_labeled.csv")

print("=" * 50)
print("📊 LABELED DATA SUMMARY")
print("=" * 50)
print(f"Total news: {len(df)}")
print(f"\nLabel distribution:")
print(df["label"].value_counts())
print(f"\nLabel percentage:")
print((df["label"].value_counts(normalize=True) * 100).round(1))
print(f"\nFirst 5 rows:")
print(df.head())
