import torch
from transformers import BertForSequenceClassification, BertTokenizer, pipeline
from utils.preprocess import preprocess_tweet

# This is the path to directory where fine-tuned model is saved
model_path = "C:\\Users\\Shelender Kumar\\Downloads\\Rewaa"

# Fine-tuned model and toenizer are loaded
model = BertForSequenceClassification.from_pretrained(model_path)
tokenizer = BertTokenizer.from_pretrained(model_path)

# A mapping is defined from sentiment labels to human-readable names
SENTIMENT_LABELS = {0: 'Negative', 1: 'Positive'}


def predict_sentiment(text):
    preprocessed_text = preprocess_tweet(text)

    # The input text is tokenized
    inputs = tokenizer.encode_plus(
        text,
        None,
        add_special_tokens=True,
        max_length=256,
        padding='max_length',
        return_token_type_ids=True,
        return_attention_mask=True,
        truncation=True
    )

    # Input is converted to PyTorch tensors
    input_ids = torch.tensor(inputs['input_ids'], dtype=torch.long).unsqueeze(0)
    attention_mask = torch.tensor(inputs['attention_mask'], dtype=torch.long).unsqueeze(0)

    # Forward pass through the model
    outputs = model(input_ids=input_ids, attention_mask=attention_mask)
    predicted_label_id = torch.argmax(outputs.logits).item()

    # Predicted label ID is mapped to sentiment class label
    predicted_sentiment = SENTIMENT_LABELS[predicted_label_id]
    return predicted_sentiment
