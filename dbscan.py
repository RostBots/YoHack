import nltk
from nltk.corpus import stopwords
from sklearn.cluster import DBSCAN
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import TweetTokenizer
import pandas as pd

tokenizer = TweetTokenizer()

def preprocess(text):
    return ' '.join(tokenizer.tokenize(text.lower()))

def check_question(text): 
    stop_words = stopwords.words('english')
    data = pd.read_csv('questions.csv')
    
    X = list(data['Question'].apply(preprocess))
    y = list(data['Answer'].apply(preprocess))
    
    X.append(text)
    y.append('')
    
    count_vect = CountVectorizer(max_features=5000, stop_words=stop_words)
    X_count = count_vect.fit_transform(X)

    clustering = DBSCAN(eps=1, min_samples=2)
    clustering.fit(X_count)

    clusters = clustering.labels_
    
    ans = {}
    for i in range(len(clusters) - 1):
        if clusters[i] == clusters[-1]:
            ans[X[i]] = y[i]
        
    return ans
