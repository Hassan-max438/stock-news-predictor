# 📈 Stock News Sentiment Predictor

Fine-tuned FinBERT model that predicts stock price movement (spike/decline) from news headlines.

## 🚀 Live Demo
**Try it here:** [Stock News Predictor](https://a4be82721aa19208bb.gradio.live)

Type any news headline → get instant spike/decline prediction!

## 📊 Results
- **Accuracy:** 57.81%
- **Spike F1:** 0.47
- **Decline F1:** 0.65

## 🛠️ Pipeline
1. Fetch news from Massive API (month-by-month)
2. Fetch 5-min price bars
3. Label: spike (>0.1%), decline (<-0.1%), neutral
4. Fine-tune FinBERT (binary classification)

## 📁 Files
- `stock_pipeline.py` — Main data pipeline (news + prices + labeling)
- `fetch_news.py` — News fetch script
- `check_results.py` — Data validation
- `app.py` — Gradio web interface
- `finbert_training.ipynb` — Colab training notebook

## 🔧 Installation
```bash
pip install -r requirements.txt
