import math 
import sys 
import connectdb as db 
import pandas as pd 
import numpy as np 
import connectdb as cnndb
import tfidf
import requests

sys.stdout.reconfigure(encoding='utf-8')

data = db.data_json

des = [i['description'] for i in data]

def get_product_byChatBot(string):
    index = tfidf.FindTheMostForChatBot(string)
    result = cnndb.query(f"SELECT name, description, price FROM tbl_Products WHERE id = {index + 1}")
    result = np.array(result)
    response = "Sản phẩm: " + result[0][0] + ", Mô tả: " +  result[0][1] + ', Giá: ' + str(result[0][2])
    return response
