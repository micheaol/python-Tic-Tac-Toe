from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
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


def find_index(id):
    for i, post in enumerate(my_post):
        if post["id"] == id:
            return i

@app.get("/")
def root():
    return {"message": "Welcome to my python api"}


@app.get("/posts")
def get_post():
    return { "data": my_post}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    return {"data": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    dict_post = post.dict()
    dict_post["id"] = randrange(0, 100)
    my_post.append(dict_post)
    return {"data": dict_post}


@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    my_post.pop(index)
    return {"data": "post deleted successfully"}

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    post_dict = post.dict()

    post_dict["id"] = id
    my_post[index] = post_dict
    return {"data": post_dict}
