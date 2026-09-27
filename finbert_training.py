from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

model_path = "hassan1256/finbert_stock_model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)
model.eval()

def predict(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
    probs = torch.softmax(outputs.logits, dim=-1)
    pred = torch.argmax(probs, dim=-1).item()
    conf = probs[0][pred].item()
    label = "spike 📈" if pred == 0 else "decline 📉"
    return f"{label} ({conf:.2%})"

print(predict("Apple beats earnings expectations"))
print(predict("Apple faces major lawsuit"))
print(predict("Apple stock drops after weak sales"))
