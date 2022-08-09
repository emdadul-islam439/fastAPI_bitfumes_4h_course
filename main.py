from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index():
    return { "Data" : "Index Page" }

@app.get("/about")
def about():
    return { "Data" : "About Page" }