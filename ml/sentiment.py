from textblob import TextBlob

def analyze_sentiment(text):
    if not text:
        return {"label":"Not available","polarity":0}
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.1:
        label = "Positive"
    elif polarity < -0.1:
        label = "Negative"
    else:
        label = "Neutral"
    return {"label":label, "polarity":round(polarity,3)}
