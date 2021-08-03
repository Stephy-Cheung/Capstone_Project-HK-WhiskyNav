# %%
import re
import pandas as pd
import numpy as np
from nltk import word_tokenize          
from nltk.stem import WordNetLemmatizer 
from nltk import pos_tag
from nltk.corpus import stopwords, wordnet
from string import punctuation
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt 
import pickle

# %%

# read whisky reviews
doc_table = pd.read_csv("./dataset/whisky_review.csv")
corpus = doc_table["reviews"].fillna('')
# %%
# print word cloud of tdidf of reviews of whisky using tdidf

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
        words = [word for word in words if word not in _stopwords]
        words = [word for word in words if not any(map(str.isnumeric, word))]
        tags = pos_tag(words)
        lemma_words = []
        
        for i,e in enumerate(tags):
            tag = self.get_wordnet_pos(e[1])
            lemma_words.append(self.wnl.lemmatize(e[0], pos=tag))
        return lemma_words
    
    def __call__(self, articles):
        return self.lemma(word_tokenize(articles))
    
def print_word_cloud(index):
    new_vectorizer = None
    with open('./model/vectorizer.pkl', 'rb') as fin:
        new_vectorizer = pickle.load(fin)
    vector = new_vectorizer.transform([corpus[index]]).toarray()
    names = new_vectorizer.get_feature_names()
    names = pd.DataFrame(names,columns=['names'])
    vector = pd.DataFrame(vector[0],columns=['freq'])
    tdidf_table = pd.concat([names,vector],axis=1).set_index('names')
    wordcloud = WordCloud(width=1000, height=500,min_word_length=2).generate_from_frequencies(tdidf_table['freq'])
    plt.figure( figsize=(20,10), facecolor='k')
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()
    
print_word_cloud(0)
# %%
