from typing import List
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session


from app import models, schemas, utils
from app.database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Method for the application root
@app.get("/")
async def root():
    return {"Message": "Hello World"}


# Method for getting all posts
@app.get("/posts", response_model=List[schemas.PostResponse])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


# Method for creating posts
# Create a new post based on the data given in api call
# **post.model_dump() converts the Pydantic model post into a dictionary and unpacks it
# Then, add the new post to the db, commit (db.commit()) and fetch (db.refresh())
@app.post(
    "/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# Method for creating users
@app.post(
    "/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse
)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Update password to the hashed password
    user.password = utils.hash(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# Method to get specific post by id
@app.get("/posts/{id}", response_model=schemas.PostResponse)
async def get_post_by_id(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found",
        )
    return post


# Method to delete specific post by id
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post_by_id(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found",
        )
    post_query.delete(synchronize_session=False)
    db.commit()


# Method to update specific post by id
@app.put("/posts/{id}", response_model=schemas.PostResponse)
async def update_post_by_id(
    id: int, post: schemas.PostCreate, db: Session = Depends(get_db)
):
    updated_post = db.query(models.Post).filter(models.Post.id == id).first()

    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )

    for key, value in post.model_dump().items():
        setattr(updated_post, key, value)

    db.commit()
    db.refresh(updated_post)
    return updated_post
