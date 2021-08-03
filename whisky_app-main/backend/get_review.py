# %%
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import json
from nltk import word_tokenize          
from nltk import word_tokenize          
from nltk.stem import WordNetLemmatizer 
from nltk import pos_tag
from nltk.corpus import stopwords, wordnet
from string import punctuation
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from lemmaTokenizer import LemmaTokenizer
# %%
# read url and id of top 100 whisky 
df = pd.read_csv('./dataset/top100_whisky.csv')
df["masterofmalt_id"] = df["masterofmalt_id"].fillna(False)
# %%
# get reviews 
corpus = []
whisky_list = []
count = 0
for whisky_id in df["masterofmalt_id"]:
    if whisky_id:
        whisky_id = str(int(whisky_id))
        URL = "https://www.masterofmalt.com/api/v2/reviews/" + whisky_id + "?format=json"
        reviews = requests.get(URL)
        reviews = json.loads(reviews.text)
        total_reviews = ''
        for data in reviews['data']:
            if 'review' in data.keys():
                review = data['review'].strip().lower()
                review = re.sub(r'[\n\r]',"",review)
                review = re.sub(r'[^\w]+(\w)', r' \1',review)
                review = re.sub(r'(\w)[^\w]+', r'\1 ',review)
                total_reviews = total_reviews + " " + review
            
        corpus.append(total_reviews)
    else:
        corpus.append('')
    print(count)
    count += 1
# %%
# save reviews as whisky_review
df['reviews'] = corpus
doc_table = df[["masterofmalt_id", "reviews"]]
doc_table.to_csv('./dataset/whisky_review.csv', index=False)   

# %%
# stopwords: whisky distiller name, whisky, year, old, like, taste

vectorizer = TfidfVectorizer(tokenizer=LemmaTokenizer())

vectorizer.fit(corpus)

with open('./model/vectorizer.pkl', 'wb') as fin:
     pickle.dump(vectorizer, fin)


# %%
