#%%

import json
import pandas as pd
import seaborn as sns
import base64
import io 
import matplotlib.pyplot as plt

def price_whisky(index):
    f = open("./dataset/pricecom_details.txt")
    whisky = json.load(f)

    shop_list = whisky[str(index)][0]
    address_list = whisky[str(index)][1]
    price_list = whisky[str(index)][2]

    return [shop_list, address_list, price_list]

def hkls_whisky(index):
    hkls_details = pd.read_csv('./dataset/hkls_details.csv')
    name, address, price = None, None, None

    if hkls_details['Stock'][index] == True:
        name = 'Hong Kong Liquor Store (10 Stores with online shop)'
        address = 'https://www.hkliquorstore.com/locations'
        price = hkls_details['Price'][index]

    return [name,address,price]

def watsons_whisky(index):
    watsons_details = pd.read_csv('./dataset/watsons_details.csv')
    name, address, price, volume = None, None, None, None

    if watsons_details['Stock'][index] == True:
        name = "Watson's wine  (23 Stores with online shop)"
        address = 'https://www.watsonswine.com/en'
        price = watsons_details['Price'][index]
        volume = watsons_details['Volume'][index]

    return [name,address,price,volume]

def stores_data(index):
    pricecom = price_whisky(index)
    
#%%

def price_chart(x):

    shop_list, address_list, price_list = price_whisky(x)
    volume = watsons_whisky(x)[3] 
    
    if hkls_whisky(x)[0] != None:
        shop_list.append(hkls_whisky(x)[0])
        address_list.append(hkls_whisky(x)[1])
        price_list.append(hkls_whisky(x)[2])

    if watsons_whisky(x)[0] != None:
        shop_list.append(watsons_whisky(x)[0])
        address_list.append(watsons_whisky(x)[1])
        price_list.append(watsons_whisky(x)[2])

    w_info = pd.DataFrame({"Shop": shop_list, "Address": address_list, "Price": price_list})
    sns.histplot(data=w_info, x='Price')
    
    # plt.show()
    pic_IObytes = io.BytesIO()
    plt.savefig(pic_IObytes,  format='png')
    pic_IObytes.seek(0)

    sorted_table = w_info.sort_values(by=['Price'],ignore_index= True)
    
    if isinstance(sorted_table, pd.Series):
        sorted_table = sorted_table.to_frame().T
        
    # print(sorted_table)
    # for i in range(len(sorted_table['Shop'])):
    #     print(i+1,'=====================================')
    #     line =40 - len(sorted_table['Shop'][i])
    #     print(sorted_table['Shop'][i], (' ')*line, sorted_table['Price'][i])
    #     print(sorted_table['Address'][i])
    #     print()
    return [base64.b64encode(pic_IObytes.getvalue()).decode("utf-8").replace("\n", "")
, sorted_table, volume]
    


# %%

# %%