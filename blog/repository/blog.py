from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status

def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    if len(blogs) == 0:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Blog list is empty!")
    else:
        return blogs


def create(request: schemas.Blog, db: Session):
    new_blog = models.Blog(title = request.title, body = request.body, user_id = 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def destroy(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id no. {id} is not found!")

    blog.delete(synchronize_session=False)
    db.commit()
    return "Done"


def update(id: int, request: schemas.Blog, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id no. {id} not found!")
    
    updated_request = {}
    if request.title:
        updated_request['title'] = request.title
    if request.body:
        updated_request['body'] = request.body


def show(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Blog no. {id} not found!")
        # response.status_code = status.HTTP_404_NOT_FOUND #from fastapi import Response
        # return { "detail" : f"Blog no. {id} not found!" }
    else:
        return blog