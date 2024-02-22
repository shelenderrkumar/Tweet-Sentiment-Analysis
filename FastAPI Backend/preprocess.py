import re
import string

def preprocess_tweet(tweet):
    # URLs are removed
    text = re.sub(r'https?://\S+', '', text)

    # handles are removed
    text = re.sub(r'@\w+', '', text)

    # Punctuation is removed using string's in-built punctuation method
    text = text.translate(str.maketrans('', '', string.punctuation))

    return text
