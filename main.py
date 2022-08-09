from fastapi import FastAPI

app = FastAPI()


# limit and published is optional
@app.get("/blog")
def index(limit: int = 5, published: bool = True):
    if published:
        return { "Data" : f"Showing {limit} published blogs." }
    else:
        return { "Data" : f"Showing {limit} blogs." }


# limit is required, published is optional
@app.get("/blog")
def index(limit: int, published: bool = True):
    if published:
        return { "Data" : f"Showing {limit} published blogs." }
    else:
        return { "Data" : f"Showing {limit} blogs." }


# limit and published both are required
@app.get("/blog")
def index(limit: int, published: bool):
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