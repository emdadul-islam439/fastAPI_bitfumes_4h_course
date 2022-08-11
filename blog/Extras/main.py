from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import uvicorn

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




# for debugging purposes, you can run the file in different port
# import uvicorn
# type 'python3 main.py' to run
# can output as the other methods

# if __name__ == "__main__":
#     uvicorn.run(app, host = "127.0.0.1", port = 9000)