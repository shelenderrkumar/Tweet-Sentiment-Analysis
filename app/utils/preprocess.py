import re
import string


def preprocess_tweet(text):
    """Preprocesses the given text.

    Args:
      text: Text to be preprocessed.

    Returns:
      Preprocessed text.
    """

    # URLs are removed
    text = re.sub(r"https?://\S+", "", text)

    # Handles are removed
    text = re.sub(r"@\w+", "", text)

    # Punctuation is removed using string's in-built punctuation method
    text = text.translate(str.maketrans("", "", string.punctuation))

    return text
