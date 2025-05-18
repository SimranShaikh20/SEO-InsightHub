from sklearn.feature_extraction.text import TfidfVectorizer

def analyze_keywords(text, top_n=10):
    vectorizer = TfidfVectorizer(stop_words='english', max_features=top_n)
    tfidf_matrix = vectorizer.fit_transform([text])
    features = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.toarray()[0]
    return sorted(zip(features, scores), key=lambda x: x[1], reverse=True)
