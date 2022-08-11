# from typing import Optional
from typing import Optional, List
from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    body: str
    class Config:
        orm_mode = True


class UpdatedBlog(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None


class User(BaseModel):
    name: str
    email: str
    password: str

class UserInfo(BaseModel):
    name: str
    email: str
    class Config:
        orm_mode = True

class ShowUser(UserInfo):
    blogs: List[Blog] = []


class ShowBlog(BaseModel):
    title: str
    body: str
    creator: UserInfo
    
    class Config():
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str