import re


def normalize_text(text):
    text = text.lower()
    text = re.sub(r'https?://\S+|www\.\S+', '<URL>', text)
    text = re.sub(r'\b\d+\b', '<NUM>', text)
    text = re.sub(r'[^\w\s<>]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()

    return text