# %%
import re
import pandas as pd
import numpy as np
from nltk import word_tokenize          
from nltk.stem import WordNetLemmatizer 
from nltk import pos_tag
from nltk.corpus import stopwords, wordnet
from string import punctuation
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt 
import pickle
from sklearn.cluster import KMeans
# %%

df = pd.read_csv('./dataset/whisky_flavour.csv')
df = df.fillna('')
# %%
whisky_list = pd.read_csv('./dataset/top100_whisky.csv')
whisky_name = whisky_list['Name']
total_names = []
for name in whisky_name:
    names = word_tokenize(name.lower())
    total_names = total_names + names

_stopwords = set(stopwords.words('english') + list(punctuation) + ['whisky', 'whiskey', 'year', 'old', 'like','taste', 'scotch', 'doublewood', 'bottle','drink', 'best'] + total_names)

class LemmaTokenizer():
    def __init__(self):
        self.wnl = WordNetLemmatizer()
        
    def get_wordnet_pos(self, tag):
        if tag.startswith('J'):
            return wordnet.ADJ
        elif tag.startswith('V'):
            return wordnet.VERB
        elif tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN  

    def lemma(self, words):
        words = list(set([word for word in words if word not in _stopwords]))
        words = [word for word in words if not any(map(str.isnumeric, word))]
        tags = pos_tag(words)
        lemma_words = []
        
        for i,e in enumerate(tags):
            tag = self.get_wordnet_pos(e[1])
            lemma_words.append(self.wnl.lemmatize(e[0], pos=tag))
        return lemma_words
    
    def __call__(self, articles):
        return self.lemma(word_tokenize(articles))

nose_vectorizer = CountVectorizer(tokenizer=LemmaTokenizer())
palate_vectorizer = CountVectorizer(tokenizer=LemmaTokenizer())
finish_vectorizer = CountVectorizer(tokenizer=LemmaTokenizer())

nose_vectors = nose_vectorizer.fit_transform(df['noses']).toarray()
palate_vectors = palate_vectorizer.fit_transform(df['palates']).toarray()
finish_vectors = finish_vectorizer.fit_transform(df['finishs']).toarray()

vectors = np.concatenate([nose_vectors,palate_vectors,finish_vectors], axis=1)


# %%
kmeans = KMeans(n_clusters=10, random_state=0).fit(vectors)
# %%

kmeans.predict(vectors[:99])
# %%
