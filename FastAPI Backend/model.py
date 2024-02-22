from transformers import BertForSequenceClassification, BertTokenizer, pipeline
from preprocess import preprocess_tweet

model_path = ""

# Load the trained model
model = BertForSequenceClassification.from_pretrained(model_path)
tokenizer = BertTokenizer.from_pretrained(model_path)


def predict_sentiment(text, model_path):
    # Create a pipeline for sentiment analysis
    nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

    # Predict the sentiment of the preprocessed input text
    preprocessed_text = preprocess_tweet(text)
    result = nlp(preprocessed_text)

    # Extract the sentiment label from the result
    sentiment = result[0]['label']
    
    return sentiment
