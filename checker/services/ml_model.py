import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer

import os
import nltk
from pathlib import Path

# Point NLTK to the bundled data folder inside the project
NLTK_DATA_DIR = Path(__file__).resolve().parent.parent.parent / "nltk_data"
if str(NLTK_DATA_DIR) not in nltk.data.path:
    nltk.data.path.append(str(NLTK_DATA_DIR))

ps = PorterStemmer()


def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

tfidf = pickle.load(open('ml_models/vectorizer.pkl','rb'))
model = pickle.load(open('ml_models/model.pkl','rb'))

def spam_ham_detector(input_sms):
    # 1. Transform text
    transformed_sms = transform_text(input_sms)

    # 2. Vectorize
    vector_input = tfidf.transform([transformed_sms])

    # 3. Prediction
    result = model.predict(vector_input)[0]

    # 4. Probability
    probabilities = model.predict_proba(vector_input)[0]

    # 5. Display
    if result == 1:
        label = "Spam"
        confidence = probabilities[1] * 100
    else:
        label = "Not Spam"
        confidence = probabilities[0] * 100

    return {
        "prediction": label,
        "confidence": round(confidence, 2),
    }
