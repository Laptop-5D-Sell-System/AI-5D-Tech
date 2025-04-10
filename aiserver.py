import sys
from fastapi.middleware.cors import CORSMiddleware
import searchquery as sq
import connectdb as db
import tfidf 
import connectdb as cnndb
from fastapi import FastAPI, Request
from google.cloud import dialogflow
import os
import uuid
from fastapi.responses import JSONResponse
from google.oauth2 import service_account
from google.auth.transport.requests import Request as rq
import requests

sys.stdout.reconfigure(encoding='utf-8')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Nam_3_Ky_2\\DACN\\AI\\key-api-chatbot-aiagent.json"

SERVICE_ACCOUNT_FILE = "C:\\Nam_3_Ky_2\\DACN\\AI\\key-api-chatbot-aiagent.json"
PROJECT_ID = "nqd-chatbot-nv9d"
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

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

def get_email_by_id(account_id):
    result = cnndb.query(f"SELECT name FROM tbl_Products WHERE id = {account_id}")
    return result[0][0] if result else "Không tìm thấy email"

def get_order_by_userid(order_id):
    QUERY = f'''
    select pro.name, odt.quantity, pro.price, od.status, od.total
    from tbl_Orders as od 
    join tbl_Order_Items as odt
    on odt.order_id = od.id
    join tbl_Products as pro
    on pro.id = odt.product_id
    where od.id = {order_id}
    '''
    columns_query = ["productName", "quantity", "price", "status", 'total']
    data_order = cnndb.convert_to_json(cnndb.query(QUERY), columns_query)
    return data_order

# Methods
@app.get('/')
def root():
	return {"API is running"}

# Get sản phẩm bằng query
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

# Get sản phẩm tương đồng
@app.get('/similar/{id}')
def findSimilarity(id: int):
	try:
		products = db.data_json
		top5 = tfidf.FindTop5SimilarProducts(id)
		pros = [products[i] for i in top5]
		return {'mess' : 'Các sản phẩm có thể bạn sẽ quan tâm: ', 'pros' : pros, 'httpStatus': 200}
	except Exception as ex:
		return {'mess': f'Có lỗi xảy ra: + {ex}', 'httpStatus' : 500}

@app.post("/chat")
async def chat(request: Request):
    payload = await request.json()
    query_text = payload["queryResult"]["queryText"]
    intent = payload["queryResult"]["intent"]["displayName"]
    parameters = payload["queryResult"]["parameters"]
    print(f"Query: {query_text}, Intent: {intent}, Params: {parameters}")
    session_id = payload.get("session", str(uuid.uuid4()))
    
    # Itent lấy product by id
    if intent == "email_id":
        account_id = parameters.get('number')
        if account_id:
            email = get_email_by_id(int(account_id))
            print(email)
            return JSONResponse({"fulfillmentText" : email})
        else:
            return JSONResponse({"error": "Có lỗi xảy ra! Vui lòng thử lại sau!"})

    # Intent lấy order by id
    if intent == "order_id":
        order_id = parameters.get('number')
        if order_id:
            order = get_order_by_userid(int(order_id))
            if order == []:
                return JSONResponse({"fulfillmentText" : "Đơn hàng không tồn tại! Vui lòng thử lại sau !"})
            print(order)
            return JSONResponse({"fulfillmentText" : str(order)})
        else:
            return JSONResponse({"error": "Có lỗi xảy ra! Vui lòng thử lại sau!"})

    return JSONResponse({"fulfillmentText": "Xin lỗi, tôi không hiểu, bạn có thể nói rõ hơn được không ?"})

@app.get('/test-chatbot')
def send_to_dialogflow(text, session_id="fixed-session-1234"):
    if session_id is None:
        session_id = str(uuid.uuid4())  

    url = f"https://dialogflow.googleapis.com/v2/projects/{PROJECT_ID}/agent/sessions/{session_id}:detectIntent"
    headers = {
        "Authorization": f"Bearer {credentials.token}",
        "Content-Type": "application/json"
    }

    payload = {
        "session": f"projects/{PROJECT_ID}/agent/sessions/{session_id}",
        "queryInput": {
            "text": {
                "text": text,
                "languageCode": "en"
            }
        }
    }
    credentials.refresh(rq())
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        response =  response.json()
        return {"mess" : response["queryResult"]["fulfillmentText"]}
    else:
        return {"error": response.text}