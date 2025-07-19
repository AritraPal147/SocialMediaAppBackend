import enum
from random import randrange
from typing import Optional
from fastapi import Body, FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

# Entity class for new_post, containing 2 parameters, title -> str and content -> str
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"id": 1, "title": "Title of Post 1", "content": "Content of Post 1"}, 
            {"id": 2, "title": "Title of Post 2", "content": "Content of Post 2"}]


def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post

def find_index_post(id):
    for i, post in enumerate(my_posts):
        if (post['id'] == id):
            return i
        

# Method for the application root
@app.get("/")
async def root():
    return {"Message": "Hello World"}


# Method for getting all posts
@app.get("/posts")
async def get_posts():
    return {"data": my_posts}


# Method for creating posts
@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


# Method to get specific post by id
@app.get("/posts/{id}")
async def get_post_by_id(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} not found")
    return {"post_details": post}


# Method to delete specific post by id
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post_by_id(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    my_posts.pop(index)


# Method to update specific post by id
@app.put("/posts/{id}")
async def update_post_by_id(id: int, updated_post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    updated_post_dict = updated_post.model_dump()
    updated_post_dict["id"] = id
    my_posts[index] = updated_post_dict
    return {"updated post": updated_post_dict}