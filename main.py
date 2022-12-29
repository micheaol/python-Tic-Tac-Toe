from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    rating: Optional[int] = None


my_post = [
    {
        "id": 1,
        "title": "Post 1",
        "content": "Content of post 1",
    },
    {
        "id": 2,
        "title": "Post 2",
        "content": "Content of post 2",
    },
    {
        "id": 3,
        "title": "Post 3",
        "content": "Content of post 3",
    },
]

@app.get("/")
def root():
    return {"message": "Welcome to my python api"}


@app.get("/posts")
def get_post():
    return { "data": my_post}


@app.post("/posts")
def create_post(post: Post):
    post = post.dict()
    print(post)
    return {"data": post}