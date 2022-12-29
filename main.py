from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

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

def find_post(id):
    for post in my_post:
        if post["id"] == int(id):
            return post



@app.get("/")
def root():
    return {"message": "Welcome to my python api"}


@app.get("/posts")
def get_post():
    return { "data": my_post}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    return {"data": post}


@app.post("/posts")
def create_post(post: Post):
    dict_post = post.dict()
    dict_post["id"] = randrange(0, 100)
    my_post.append(dict_post)
    print(my_post)
    return {"data": dict_post}