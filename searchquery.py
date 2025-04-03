import sys
import naviebayes as nvb 
import math

sys.stdout.reconfigure(encoding='utf-8')

# Lấy ra tất cả các tên của sản phẩm 
def getAllName(products):
    arrName = [product['name'] for product in products]
    return arrName

# Tính độ tương đồng bằng tên
def similarity_name(name, products, stringToUnique):
    arrScore = []
    arrWord_name = nvb.CatChuoi(name)
    for string in getAllName(products):
        score = 0
        for word in arrWord_name:
            score += math.log(nvb.probability(word, string, stringToUnique))
        arrScore.append(score)
    return arrScore

# Tìm kiếm sản phẩm bằng search
def search(query, products, stringToUnique):
    arrScore = similarity_name(query, products, stringToUnique)
    # print(arrScore)
    arrIndex = []
    length = len(nvb.CatChuoi(query))

    for i, score in enumerate(arrScore): 
        if score / length > -5:
            arrIndex.append(i)
    if arrIndex == []:
        return None
    arrIndex.sort(key=lambda i: arrScore[i], reverse=True)
    suggestedArray = [products[index] for index in arrIndex]
    return suggestedArray
