from fastapi import FastAPI, Depends, status, HTTPException
from .database import engine, SessionLocal
from . import schemas, models
from sqlalchemy.orm import Session


app = FastAPI()
models.Base.metadata.create_all(engine)

def get_db():   
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title = request.title, body = request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blog", status_code=status.HTTP_200_OK)
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    if len(blogs) == 0:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Blog list is empty!")
    else:
        return blogs


@app.get("/blog/{id}", status_code=status.HTTP_200_OK)
def show(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Blog no. {id} not found!")
        # response.status_code = status.HTTP_404_NOT_FOUND #from fastapi import Response
        # return { "detail" : f"Blog no. {id} not found!" }
    else:
        return blog

