from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index():
    return { "Data" : "Index Page" }


@app.get("/blog/{id}")
def show(id: int):
    return { "Data" : f"Blog no. {id}" }    


@app.get("/blog/{id}/comments")
def comments(id: int):
    return { 
        "ID" : id,
        "Comments" : ["Comment 1", "Comment 2"] 
    }


@app.get("/blog/unplublished")
def unpublished():
    return { "Data" : "Some unpublished blogs" }