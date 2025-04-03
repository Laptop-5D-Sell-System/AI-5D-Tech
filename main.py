import aiserver as aiserver
import uvicorn
import chatbot as cb

if __name__ == "__main__":
	uvicorn.run(cb.app, host='localhost', port = 8080)