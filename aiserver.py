import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import searchquery as sq
import connectdb as db
import tfidf 

sys.stdout.reconfigure(encoding='utf-8')

app = FastAPI()

# Start port
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]
 # CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Methods
@app.get('/')
def root():
	return {"API is running"}

@app.get('/search/{query}')
def searchQuery(query : str):
	try:
		products = db.data_json
		stringToUnique = 'name'
		pros = sq.search(query, products, stringToUnique)
		if pros == None:
			return {'mess' : 'Không tìm thấy sản phẩm !', 'httpStatus' : 404}
		return {'pros': pros, 'mess' : 'Kết quả tìm kiếm', 'httpStatus' : 200}
	except Exception as ex:
		return {'mess': f'Có lỗi xảy ra: + {ex}', 'httpStatus' : 500}


@app.get('/similar/{id}')
def findSimilarity(id: int):
	try:
		products = db.data_json
		top5 = tfidf.FindTop5SimilarProducts(id)
		pros = [products[i] for i in top5]
		return {'mess' : 'Các sản phẩm có thể bạn sẽ quan tâm: ', 'pros' : pros, 'httpStatus': 200}
	except Exception as ex:
		return {'mess': f'Có lỗi xảy ra: + {ex}', 'httpStatus' : 500}

