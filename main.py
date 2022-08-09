import imp
from fastapi import FastAPI
from typing import Optional

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