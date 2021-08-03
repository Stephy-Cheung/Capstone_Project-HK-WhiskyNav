# %%
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
import numpy as np
import re
import pickle
# %%
def get_table(soup):
    table = soup.select('table')
    table_rows = table[0].find_all('tr')

    l = []

    for i, tr in enumerate(table_rows):
        if i == 0:
            th = tr.find_all('th')
            row = [tr.text.strip("\n\t") for tr in th]
            column = row
        else:
            td = tr.find_all('td')
            row = [tr.text.strip("\n\t") for tr in td]
            l.append(row)
    table = pd.DataFrame(l, columns=column)
    return table

# %%
originalURL = "https://www.whiskybase.com/whiskies/new-releases"
driver = webdriver.Chrome("./chromedriver")
driver.get(originalURL)
html = driver.page_source
soup = BeautifulSoup(html,'html.parser')
years = soup.select("[data-filter='bottle_date_year'] option")
years = [i.text for i in years]
count = 1
for year in years: 
    if count > 1: 
        URL = originalURL + "?style=table&bottle_date_year=" + year
        driver.get(URL)
        html = driver.page_source
        soup = BeautifulSoup(html,'html.parser')
        total_table = pd.concat([total_table, get_table(soup)])
    else:
        total_table = get_table(soup) 
     
    count += 1
    
# %%
total_table.to_csv('./dataset/whisky_database.csv', index=False)

# %%
# load table
# break out num from letter
def space_num(word):
    word = re.sub(r'([^\d\s]+)(\d+)', r'\1 \2', word)
    word = re.sub(r'(\d+)([^\d\s]+)', r'\1 \2', word)
    return word.strip()

def clean_str(text):
    text = ''.join([word for word in text if word not in string.punctuation])
    text = text.lower()
    text = ' '.join([space_num(word) for word in text.split()])
    return text

df = pd.read_csv('whisky_database.csv')
df = df.drop(columns=['Unnamed: 0','Unnamed: 10'])
df = df.drop_duplicates(subset=['Name'])
df['Cleaned_Name'] = df['Name'].transform(clean_str)


# %%
df
# %%
# recommendation search using consine similarity
    
def search_top_5(text, df):
    # don't remove stopwords because whisky brand may not be English
    # stops = stopwords.words('english')
    
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(df['Cleaned_Name'])
    vector = vectorizer.transform([clean_str(text)])
    csim = cosine_similarity(vector, vectors)
    top_match = csim.argsort()[0][::-1]
    count = 0
    for i in top_match:
        if count < 5 and csim[0][i] > 0.5:
            count += 1
        else:
            break
    return df[['Name','Strength']].iloc[top_match[:count]], csim[0][top_match[:count]]
# %%
print(search_top_5('Laphroaig 10 Cask Strength', df))
# %%
