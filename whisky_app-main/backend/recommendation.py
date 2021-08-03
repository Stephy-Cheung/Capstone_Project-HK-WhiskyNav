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
from lemmaTokenizer import LemmaTokenizer

# %%

df = pd.read_csv('./dataset/whisky_flavour.csv')
df = df.fillna('')
# %%
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
