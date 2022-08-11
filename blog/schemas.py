# from typing import Optional
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