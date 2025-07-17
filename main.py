from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

# Entity class for new_post, containing 2 parameters, title -> str and content -> str
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


# Method for the application root
@app.get("/")
async def root():
    return {"Message": "Hello World"}


# Method for getting all posts
@app.get("/posts")
async def get_posts():
    return {"Data": "This is all the data for your application"}


# Method for creating posts
@app.post("/posts")
async def create_post(post: Post):
    return {"data": post}