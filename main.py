import aiserver as aiserver
import uvicorn

if __name__ == "__main__":
	uvicorn.run(aiserver.app, host='localhost', port = 8080)
