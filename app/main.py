from typing import List
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session


from app import models, schemas, utils
from app.database import engine, get_db
from app.routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)


# Method for the application root
@app.get("/")
async def root():
    return {"Message": "Hello World"}
