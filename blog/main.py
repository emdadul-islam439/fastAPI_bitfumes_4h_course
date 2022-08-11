from distutils.util import execute
from fastapi import FastAPI, Depends, status, HTTPException
from .database import engine, SessionLocal
from . import schemas, models
from sqlalchemy.orm import Session
from typing import List
from .hashing import Hash

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


@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id no. {id} is not found!")

    blog.delete(synchronize_session=False)
    db.commit()
    return "Done"


@app.put("/blog/{id}", status_code= status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.UpdatedBlog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id no. {id} not found!")
    
    updated_request = {}
    if request.title:
        updated_request['title'] = request.title
    if request.body:
        updated_request['body'] = request.body

    # raw code
    # blog.update({"title" : "updated title", "body": "updated body"})  

    # blog.update(request.dict()) will not be good choice, request.dict() updates all 'not given' field as 'null'
    # But we want every not given field as usual
    blog.update(updated_request)

    db.commit()
    return  "Updated!"



@app.get("/blog", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    if len(blogs) == 0:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Blog list is empty!")
    else:
        return blogs


@app.get("/blog/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def show(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Blog no. {id} not found!")
        # response.status_code = status.HTTP_404_NOT_FOUND #from fastapi import Response
        # return { "detail" : f"Blog no. {id} not found!" }
    else:
        return blog


@app.post("/user", status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name = request.name, email = request.email, password = Hash.get_password_hash(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/user/{id}", status_code=status.HTTP_200_OK, response_model= schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    user_info = db.query(models.User).filter(models.User.id == id)

    if not user_info.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"User with id no. {id} not found!")

    return user_info.first()