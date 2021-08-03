# %%
import re
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
# %%

df = pd.read_csv('./dataset/whiskies_b.csv')
df['Distillery'] = df['Distillery'].transform(lambda x: x.lower())

# Scale falvours score
scaler = MinMaxScaler()
flavours = ['Body','Sweetness','Smoky','Medicinal', 'Tobacco', 'Honey', 'Spicy', 'Winey', 'Nutty', 'Malty', 'Fruity', 'Floral']
df[flavours] = scaler.fit_transform(df[flavours])

# %%
def similarity(df, Distillery, reverse=False):
    Distillery = Distillery.lower()
    vectors = df[['Body','Sweetness','Smoky','Medicinal', 'Tobacco', 'Honey', 'Spicy', 'Winey', 'Nutty', 'Malty', 'Fruity', 'Floral']]
    vector = vectors[df['Distillery'] == Distillery]
    vectors = vectors[df['Distillery'] != Distillery]
        
    if len(vector) > 0:
        csim = cosine_similarity(vector, vectors)
        if not reverse:
            top_match = csim.argsort()[0][::-1]
            count = 0
            for i in top_match:
                if count < 5 and csim[0][i] > 0.7:
                    count += 1
                else:
                    break

            return df[df['Distillery'] != Distillery]['Distillery'].iloc[top_match[:count]]
        else:
            bottom_match = csim.argsort()[0]
            count = 0
            for i in bottom_match:
                if count < 5 and csim[0][i] < 0.3:
                    count += 1
                else:
                    break
            return df['Distillery'].iloc[bottom_match[:5]]
    
    else:
        return df.iloc[-1:-2]
    
# %%
def similarity_vector(df, vector, reverse=False):
    vectors = df[['Body','Sweetness','Smoky','Medicinal', 'Tobacco', 'Honey', 'Spicy', 'Winey', 'Nutty', 'Malty', 'Fruity', 'Floral']]
    csim = cosine_similarity([vector], vectors)
    if not reverse:
        top_match = csim.argsort()[0][::-1]
        count = 0
        for i in top_match:
            if count < 5 and csim[0][i] > 0.7:
                count += 1
            else:
                break
        return df['Distillery'].iloc[top_match[:count]]
    else: 
        bottom_match = csim.argsort()[0]
        count = 0
        for i in bottom_match:
            if count < 5 and csim[0][i] < 0.3:
                count += 1
            else:
                break
        return df['Distillery'].iloc[bottom_match[:5]]
    
# %%

# recommend whiskies with different names
def recommend(index, reverse=False):    
    whisky_list = pd.read_csv('./dataset/top100_whisky.csv')
    whisky_list['New_Name'] = whisky_list['Name'].transform(lambda x: x.strip().lower())
    name = whisky_list['New_Name'].iloc[index]
    if not reverse:
        match_list = np.append([name],similarity(df, name, reverse).to_numpy())
    else:
        match_list = similarity(df, name, reverse).to_numpy()

    new_table = whisky_list[whisky_list['New_Name'].isin(match_list if len(match_list) > 0 else [])]

    if isinstance(new_table, pd.Series):
        new_table = new_table.to_frame().T
        
    new_table = new_table[new_table.index != index]

          
    # sorterIndex = dict(zip(match_list, range(len(match_list))))

    # new_table['Rank'] = new_table['New_Name'].map(sorterIndex)
        
    # new_table = new_table[new_table.index != index].sort_values(['Rank'])
    
    if len(new_table) > 0:
        return new_table[["Name","Year"]].to_dict(orient="index")
    else:
        return None
    

# %%
def recommend_vector(vector, reverse=False):
    whisky_list = pd.read_csv('./dataset/top100_whisky.csv')
    whisky_list['New_Name'] = whisky_list['Name'].transform(lambda x: x.strip().lower())
    match_list = similarity_vector(df, vector, reverse).to_numpy()
    new_table = whisky_list[whisky_list['New_Name'].isin(match_list if len(match_list) > 0 else [])]
    
    if isinstance(new_table, pd.Series):
        new_table = new_table.to_frame().T
        
    # sorterIndex = dict(zip(match_list, range(len(match_list))))

    # new_table['Rank'] = new_table['New_Name'].map(sorterIndex)
        
    # new_table = new_table.sort_values(['Rank'])
    
    if len(new_table) > 0:
        return new_table[["Name","Year"]].to_dict(orient="index")
    else:
        return None

