from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to my python api"}


@app.get("/user")
def get_user():
    return {"message": "You are the user"}


@app.post("/post")
def create_post(payLoad: dict = Body(...)):
    return payLoad