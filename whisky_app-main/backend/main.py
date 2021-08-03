from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import pathlib, os, json, pickle
import pandas as pd
from PIL import Image
from lemmaTokenizer import LemmaTokenizer
from review_wordcloud import print_word_cloud
import matplotlib.pyplot as plt
from recommend_whisky import recommend, recommend_vector
from whisky_classifier import classifier
from flask_cors import CORS
from chart import price_chart
import asyncio
import time

app = Flask(__name__)
CORS(app)

df = pd.read_csv("./dataset/top100_whisky.csv")


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/searchImage", methods=['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
        img_file = request.files['image']
        # Read the image via file.stream
        index = classifier(img_file.stream)
        if index != 'N/A': 
            df = pd.read_csv("./dataset/top100_whisky.csv")
            new_table = df.iloc[index]
            if isinstance(new_table, pd.Series):
                new_table = new_table.to_frame().T
        
            return jsonify({"whiskies": new_table[["Name","Year"]].to_dict(orient="index")})
        else:
            return jsonify({"whiskies": 'N/A'})
        
@app.route("/searchFlavours", methods=['GET', 'POST'])
def search_flavours():
   if request.method == 'POST':
        data = request.get_json()
        vector = list(data['flavours'].items())
        array = []
        for i in range(len(vector) - 1):
            array.append(vector[i][1])
        # Read the image via file.stream
        # index = classifier(img_file.stream)
        # df = pd.read_csv("./dataset/top100_whisky.csv")
        # name = df["Name"].iloc[index]
        # year = df["Year"].iloc[index]

        return jsonify({
            "recommend": recommend_vector(array, vector[-1][1]),
        })

        
@app.route("/whisky/<int:whiskyId>")
def getData(whiskyId):
    # print(f"started at {time.strftime('%X')}")
    df = pd.read_csv("./dataset/top100_whisky.csv")
    new_df = df[["Name","Year"]].iloc[whiskyId].to_dict()
    recommend_data = recommend(whiskyId)
    opposite_recommend_data = recommend(whiskyId,True)
    wordcloud = print_word_cloud(whiskyId)
    price_img, price_table, volume = price_chart(whiskyId)
    
    # recommend_data, wordcloud, [price_img, price_table] = await asyncio.gather(
    #     recommend(whiskyId),
    #     print_word_cloud(whiskyId),
    #     price_chart(whiskyId)
    # )
    
    # print(f"finished at {time.strftime('%X')}")
    
    price_table = price_table.to_dict(orient="index")

    
    return jsonify({
        "info": new_df,
        "recommend": recommend_data,
        "opposite_recommend": opposite_recommend_data,
        "wordcloud": wordcloud,
        "price_img": price_img,
        "price_table": price_table,
        "volume": volume
    })
    
if __name__ == "__main__":
    app.run()

 