from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = False

# Database connection:
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='python_api', user='postgres', password='PassWord', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection was successfull!')
        break

    except Exception as error:
        print("Database connection failed")
        print("error: ", error)
        time.sleep(3)
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
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return { "data": posts}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    return {"data": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
     cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # dict_post = post.dict()
    # dict_post["id"] = randrange(0, 100)
    # my_post.append(dict_post)
     new_post = cursor.fetchone()

     conn.commit()
     return {"data": new_post}


@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))

    deleted_post = cursor.fetchone()
    conn.commit()
    
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    return {"data": "Post has been deleted successfully"}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, (str(id))))

    updted_post = cursor.fetchone()
    conn.commit()
    
    if updted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    return {"data": updted_post}
