from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    rating: Optional[int] = None


@app.get("/")
def root():
    return {"message": "Welcome to my python api"}


@app.post("/post")
def create_post(new_post: Post):
    return new_post