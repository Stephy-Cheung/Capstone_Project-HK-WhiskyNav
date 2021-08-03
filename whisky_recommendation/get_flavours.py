# %%
import requests
from bs4 import BeautifulSoup
import pandas as pd

# %%

df = pd.read_csv('./dataset/top100_whisky.csv')
URLs = df['masterofmalt_url'].fillna('')
URLs

# %%
noses = []
palates = []
finishs = []

for URL in URLs:
    if URL != '':
        html = requests.get(URL)
        soup = BeautifulSoup(html.text,'html.parser')
        if len(soup.select('#ContentPlaceHolder1_ctl00_ctl02_TastingNoteBox_ctl00_breakDownTastingNote')) > 0:
            noses.append(soup.select('#ContentPlaceHolder1_ctl00_ctl02_TastingNoteBox_ctl00_noseTastingNote')[0].text.lower())
            palates.append(soup.select('#ContentPlaceHolder1_ctl00_ctl02_TastingNoteBox_ctl00_palateTastingNote')[0].text.lower())
            finishs.append(soup.select('#ContentPlaceHolder1_ctl00_ctl02_TastingNoteBox_ctl00_finishTastingNote')[0].text.lower())
            continue
        
    noses.append('')
    palates.append('')
    finishs.append('')
    
        
df['noses'] = noses
df['palates'] = palates
df['finishs'] = finishs

table = df[['masterofmalt_id', 'noses', 'palates','finishs']]
table.to_csv('./dataset/whisky_flavour.csv',index=False)


# %%
