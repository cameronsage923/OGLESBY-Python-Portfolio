import streamlit as st

# Sentiment functions
def rule_based_sentiment(text):
    lexicon = {
        "good": 1, "great": 2, "excellent": 3,
        "bad": -2, "poor": -3, "terrible": -5
    }
    score = sum([lexicon.get(word, 0) for word in text.lower().split()])
    return "positive" if score > 0 else "negative"

# Streamlit interface
st.title("🎯 Sentiment Analyzer")
text = st.text_area("Enter your review:")

result = rule_based_sentiment(text)
st.write(f"🧠 Sentiment: **{result.upper()}**")