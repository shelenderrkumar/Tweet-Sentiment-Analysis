import torch
import sentencepiece

from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
from app.utils.preprocess import preprocess_tweet


# This is the path to directory where fine-tuned model is saved
model_path = "E:\\Shelender Kumar-Solved Assignment\\models"

# # Fine-tuned model and toenizer are loaded
model = AutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-xlm-roberta-base-sentiment")
# model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-xlm-roberta-base-sentiment")

# A mapping is defined from sentiment labels to human-readable names
SENTIMENT_LABELS = {0: 'Negative', 1: 'Neutral', 2:'Positive'}


def predict_sentiment(
    text
):
    """Fetches rows from a Smalltable.

    Retrieves rows pertaining to the given keys from the Table instance.

    Args:
      table_handle:
        An open smalltable.Table instance.

    Returns:
      A dict mapping keys to the corresponding table row data
      
    Raises:
      IOError: An error occurred accessing the smalltable.
    """
    
    preprocessed_text = preprocess_tweet(text)

    inputs = tokenizer.encode_plus(
        preprocessed_text,
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
    print(f"Outputs are: {outputs}\n")
    predicted_label_id = torch.argmax(outputs.logits).item()

    # Predicted label ID is mapped to sentiment class label
    predicted_sentiment = SENTIMENT_LABELS[predicted_label_id]
    return predicted_sentiment
