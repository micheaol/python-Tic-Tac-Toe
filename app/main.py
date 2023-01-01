from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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

# @app.get("/sqlalchemy")
# def test_alchemy(db: Session = Depends(get_db)):


#     posts = db.query(models.Post).all()
#     return {"data": posts}

@app.get("/posts")
def get_post(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    return posts


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    return post


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    #  cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))

    #  new_post = cursor.fetchone()
    #  conn.commit()



     new_post = models.Post(title=post.title, content=post.content, published=post.published)

     db.add(new_post)
     db.commit()
     db.refresh(new_post)

     return new_post


@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))

    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    post.delete(synchronize_session=False)

    db.commit()
    return {"data": "Post has been deleted successfully"}


@app.put("/posts/{id}")
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, (str(id))))

    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
