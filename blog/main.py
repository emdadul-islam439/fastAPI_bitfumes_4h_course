from distutils.util import execute
from fastapi import FastAPI, Depends, status, HTTPException
from .database import engine, get_db
from . import schemas, models
from sqlalchemy.orm import Session
from typing import List
from .hashing import Hash
from .routers import blog, user, authentication

app = FastAPI()
models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)