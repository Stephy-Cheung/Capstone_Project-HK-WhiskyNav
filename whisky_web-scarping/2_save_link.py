#%% 
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import numpy as np 
from numpy.core.fromnumeric import product

import time
from selenium import webdriver 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# ============= Load Top100_whisky =============
top100_whisky = pd.read_csv('Top100_whisky.csv')


# ====== Web scrape link in hkliqour store ======
top100_whisky['hkls_name'] = np.empty((len(top100_whisky), 0)).tolist()
top100_whisky['hkls_link'] = np.empty((len(top100_whisky), 0)).tolist()
top100_whisky['Year'] = top100_whisky['Year'].astype(str)

URL = 'https://www.hkliquorstore.com/index.php/liquor-liqueurs/whisky.html?p=72&product_list_limit=all'
html = requests.get(URL)
page =  BeautifulSoup(html.text, 'html.parser')
product_link = page.find_all(class_='product-item-link')

for i, whisky_name in enumerate(top100_whisky['Name']):
    for whisky_link in product_link: 
        if (whisky_name.lower() in whisky_link.text.lower()) and (top100_whisky['Year'][i].lower() in whisky_link.text.lower()):
            top100_whisky['hkls_name'][i] += [whisky_link.text.strip()]
            top100_whisky['hkls_link'][i] += [whisky_link.get('href')]


# ====== Web scrape link in price.com ======
def whisky_details(distillery, year):

    distillery = distillery.lower()
    URL = "https://www.price.com.hk/search.php?g=A&q="+ distillery + "+" + year
    html = requests.get(URL)
    soup = BeautifulSoup(html.text, "html.parser")

    code, name, link = [], [], []

    while True:
    
        try:
            # Whisky id in price.com
            for b in soup.find_all(class_="item-inner"):
                c = b.attrs["data-id"]
                code.append(c)
            # Whisky name
            for d in soup.find_all(class_="item club-list-row"):
                for e in d.find_all(class_="column column-02"):
                    fullname = e.find(class_="line line-01").a.text
                    name.append(fullname.strip())
            # Whisky url
            for id in code:
                search_url = "https://www.price.com.hk/product.php?p=" + id
                link.append(search_url)
        except:
            pass

        else:
            break

    return [name, link]

whisky_ls, price_name, price_link = [], [], []
for i in range(len(top100_whisky)):
    distillery = str(top100_whisky.iloc[i,0]).lower()
    year = top100_whisky.iloc[i,1]
    whisky_ls.append(whisky_details(distillery, str(year)))

for info in whisky_ls:
    price_name.append(info[0])
    price_link.append(info[1])

price = pd.DataFrame({'price_name':price_name,'price_link':price_link})
top100_whisky = pd.concat([top100_whisky,price], axis=1)

# ========web scrape link in watsons =========
page = ['https://www.watsonswine.com/en/wine-list/whiskies/c/10010211', 'https://www.watsonswine.com/en/wine-list/whiskies/c/10010211?q=%3Adiscount&page=1&resultsForPage=48&text=&sort=']

name, link, name_list, link_list = [], [], [], []

for p in page:
    # stop the banner
    capa = DesiredCapabilities.CHROME
    capa["pageLoadStrategy"] = "none"
    driver = webdriver.Chrome('../chromedriver',desired_capabilities=capa)
    driver.get(p)
    time.sleep(2)
    driver.execute_script("window.stop();")
    driver.maximize_window()    

    whiskies = driver.find_elements_by_class_name("intro")
    for i in whiskies:
        name_list.append(i.find_element_by_class_name("productName").text)
        link_list.append(i.find_element_by_tag_name("a").get_attribute("href"))

top100_whisky['wastons_name'] = np.empty((len(top100_whisky), 0)).tolist()
top100_whisky['wastons_link'] = np.empty((len(top100_whisky), 0)).tolist()

for i in range(len(top100_whisky['Name'])):
    for no in range(len(name_list)): 
        if (top100_whisky.iloc[i,0].lower() in name_list[no].lower()) and (top100_whisky.iloc[i,1].lower() in name_list[no].lower()):
            top100_whisky.iloc[i, 6].append(name_list[no])
            top100_whisky.iloc[i, 7].append(link_list[no])


# ================Save result================
top100_whisky.to_csv('Top100_whisky.csv', index= False)

