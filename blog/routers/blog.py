from fastapi import APIRouter, status, Depends, HTTPException
from typing import List 
from .. import schemas, models, database
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["Blogs"],
    prefix="/blog"
)
get_db = database.get_db


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    if len(blogs) == 0:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Blog list is empty!")
    else:
        return blogs


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title = request.title, body = request.body, user_id = 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.delete("//{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id no. {id} is not found!")

    blog.delete(synchronize_session=False)
    db.commit()
    return "Done"


@router.put("/{id}", status_code= status.HTTP_202_ACCEPTED)
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


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def show(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Blog no. {id} not found!")
        # response.status_code = status.HTTP_404_NOT_FOUND #from fastapi import Response
        # return { "detail" : f"Blog no. {id} not found!" }
    else:
        return blog