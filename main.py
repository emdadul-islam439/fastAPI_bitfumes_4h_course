from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


@app.get("/blog")
def index(limit: Optional[int] = 5, published: Optional[bool] = True):
    if published:
        return { "Data" : f"Showing {limit} published blogs." }
    else:
        return { "Data" : f"Showing {limit} blogs." }


@app.get("/blog/unpublished")
def unpublished():
    return { "Data" : "Some unpublished blogs" }


@app.get("/blog/{id}")
def show(id: int):
    return { "Data" : f"Blog no. {id}" }    


@app.get("/blog/{id}/comments")
def comments(id: int):
    return { 
        "ID" : id,
        "Comments" : ["Comment 1", "Comment 2"] 
    }


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool] = True


@app.post("/blog")
def create_blog(blog: Blog):
    return { "data" : blog }

