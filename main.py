from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to my python api"}


@app.get("/user")
def get_user():
    return {"message": "You are the user"}