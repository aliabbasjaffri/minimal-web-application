import uvicorn
from fastapi import FastAPI
from route.routes import router

app = FastAPI()
app.include_router(router)


if __name__ == "__main__":
    # Remove port=5000 and debug=True for running
    # the application in production environment
    uvicorn.run(app, host="0.0.0.0", port=5000, debug=True)
