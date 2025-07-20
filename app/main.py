from random import randrange
import time
from typing import Optional
from fastapi import Body, FastAPI, HTTPException, status
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from urllib3 import Retry

app = FastAPI()

# Entity class for new_post, containing 2 parameters, title -> str and content -> str
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

# Infinite loop to keep checking if database connection was successful or not
while True:
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(host='localhost', database='dummy', 
                                user='dummy', password='dummy', cursor_factory=RealDictCursor)
        # Cursor for interacting with the database
        cursor = conn.cursor()
        print("Database connection was successful")
        # Break out of the while loop if the db connection is successful
        break
    # If connection is not successful, then print the error and retry after 2 seconds
    except Exception as error:
        print("Connection to database failed")
        print("Error: ", error)
        time.sleep(2)


# Method for the application root
@app.get("/")
async def root():
    return {"Message": "Hello World"}


# Method for getting all posts
@app.get("/posts")
async def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}


# Method for creating posts
@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    cursor.execute(""" INSERT INTO posts (title, content, published) 
                   VALUES (%s, %s, %s) RETURNING *""", 
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


# Method to get specific post by id
@app.get("/posts/{id}")
async def get_post_by_id(id: int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (id,))
    post = cursor.fetchone()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    return {"post_details": post}


# Method to delete specific post by id
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post_by_id(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (id,))
    deleted_post = cursor.fetchone()    
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")


# Method to update specific post by id
@app.put("/posts/{id}")
async def update_post_by_id(id: int, post: Post):
    cursor.execute(""" UPDATE posts SET 
                   title = %s, content = %s, published = %s 
                   WHERE id = %s RETURNING * """, 
                   (post.title, post.content, post.published, id))
    updated_post = cursor.fetchone()    
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    return {"updated post": updated_post}

