import re
import string

def preprocess_tweet(
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

    # URLs are removed
    text = re.sub(r'https?://\S+', '', text)

    # Handles are removed
    text = re.sub(r'@\w+', '', text)

    # Punctuation is removed using string's in-built punctuation method
    text = text.translate(str.maketrans('', '', string.punctuation))

    return text
