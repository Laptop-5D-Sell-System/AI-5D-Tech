from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import connectdb as db

data = [d['description'] for d in db.data_json]

# Tính toán TF-IDF cho toàn bộ dữ liệu
vectorizer = TfidfVectorizer(lowercase=True, stop_words='english', analyzer='word', norm='l2')
tfidf_matrix = vectorizer.fit_transform(data)

# Tính toán cosine similarity giữa các vector TF-IDF
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Tìm 5 sản phẩm tương đồng nhất
def FindTop5SimilarProducts(index):
    cosine_scores = list(enumerate(cosine_sim[index - 1])) 
    cosine_scores = sorted(cosine_scores, key=lambda x: x[1], reverse=True)
    top_5 = [i for i, _ in cosine_scores[1:6]] 
    return top_5

# Tìm sản phẩm theo cấu hình của sản phẩm
def FindTheMostForChatBot(string):
    vec = vectorizer.transform([string])  
    arrScore = cosine_similarity(vec, tfidf_matrix)  
    return arrScore[0].tolist().index(max(arrScore[0]))  

