import connectdb as cnndb
from fastapi import FastAPI
from fastapi import Request
from google.cloud import dialogflow
import os
from fastapi.responses import JSONResponse
from google.oauth2 import service_account

app = FastAPI()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Nam_3_Ky_2\\DACN\\AI\\key-api-chatbot-aiagent.json"

PROJECT_ID = "nqd-chatbot-nv9d"

def detect_intent_texts(session_id, text, language_code="en"):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(PROJECT_ID, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    
    response = session_client.detect_intent(request={"session": session, "query_input": query_input})
    return response.query_result

def get_email_by_id(account_id):
    result = cnndb.query(f"SELECT email FROM Users WHERE id = {account_id}")
    return result[0][0] if result else "Không tìm thấy email"

@app.get("/get_intent")
def getIntent(string : str):
    


@app.post("/chat")
async def chat(request: Request):
    payload = await request.json()
    query_text = payload["queryResult"]["queryText"]
    intent = payload["queryResult"]["intent"]["displayName"]
    parameters = payload["queryResult"]["parameters"]

    # Nếu intent là lấy email theo ID
    if intent == "email_id":
        account_id = int(parameters['number'])
        email = get_email_by_id(account_id)
        return JSONResponse(content={"fulfillmentText": f"Email của bạn là: {email}"})

    # Nếu không phải intent đặc biệt, gọi Dialogflow xử lý
    response = detect_intent_texts("session123", query_text)
    return JSONResponse(content={"fulfillmentText": response.fulfillment_text})