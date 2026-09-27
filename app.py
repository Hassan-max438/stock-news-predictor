import gradio as gr
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

model_path = "hassan1256/finbert_stock_model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)
model.eval()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def predict_news(news_text):
    if not news_text.strip():
        return "⚠️ News text daalo"
    inputs = tokenizer(news_text, return_tensors="pt", truncation=True, max_length=128, padding=True)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
    probs = torch.softmax(outputs.logits, dim=-1)
    pred = torch.argmax(probs, dim=-1).item()
    confidence = probs[0][pred].item()
    label = "spike 📈" if pred == 0 else "decline 📉"
    return f"{label} (confidence: {confidence:.2%})"

interface = gr.Interface(
    fn=predict_news,
    inputs=gr.Textbox(label="📰 Stock News", lines=3),
    outputs=gr.Textbox(label="🎯 Prediction"),
    title="📈 Stock News Sentiment Predictor",
    examples=[
        ["Apple beats earnings expectations"],
        ["Apple faces major lawsuit"],
        ["Apple stock drops after weak sales"]
    ]
)

if __name__ == "__main__":
    interface.launch()
