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
import matplotlib
import matplotlib.pyplot as plt 
import pickle
from lemmaTokenizer import LemmaTokenizer
from PIL import Image
import base64
import io 

matplotlib.use('Agg')

# %%

# read whisky reviews
doc_table = pd.read_csv("./dataset/whisky_review.csv")
corpus = doc_table["reviews"].fillna('')
# %%  
def print_word_cloud(index):
    new_vectorizer = None
    
    # load tdidf vectorizer
    with open('./model/vectorizer.pkl', 'rb') as fin:
        new_vectorizer = pickle.load(fin)
    vector = new_vectorizer.transform([corpus[index]]).toarray()

    if any([ True if i != 0 else False for i in vector[0]]):
        names = new_vectorizer.get_feature_names()
        names = pd.DataFrame(names,columns=['names'])
        vector = pd.DataFrame(vector[0],columns=['freq'])
        tdidf_table = pd.concat([names,vector],axis=1).set_index('names')
        wordcloud = WordCloud(width=640, height=480,min_word_length=2).generate_from_frequencies(tdidf_table['freq'])
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.tight_layout(pad=0)
        
        #convert plt image to png
        pic_IObytes = io.BytesIO()
        plt.savefig(pic_IObytes,  format='png')
        plt.close()
        pic_IObytes.seek(0)
        # return base64.b64encode(pic_IObytes.read())
        # with open('./temp/wordcloud.png', mode='rb') as new_file:
        #     img = new_file.read()
        
        return base64.b64encode(pic_IObytes.getvalue()).decode('utf-8').replace("\n", "")
    else:
        return None

#%%