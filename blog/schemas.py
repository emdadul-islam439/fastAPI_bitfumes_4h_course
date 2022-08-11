# from typing import Optional
from lib2to3.pytree import Base
from typing import Optional
from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    body: str


class ShowBlog(BaseModel):
    title: str
    body: str
    
    class Config():
        orm_mode = True


class UpdatedBlog(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None


class User(BaseModel):
    name: str
    email: str
    password: str

class ShowUser(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True