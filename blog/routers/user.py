from fastapi import APIRouter, status, Depends, HTTPException
from .. import schemas, models, database
from sqlalchemy.orm import Session
from ..hashing import Hash

router = APIRouter()
get_db = database.get_db

@router.post("/user", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser, tags=["Users"])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name = request.name, email = request.email, password = Hash.get_password_hash(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/user/{id}", status_code=status.HTTP_200_OK, response_model= schemas.ShowUser, tags=["Users"])
def get_user(id: int, db: Session = Depends(get_db)):
    user_info = db.query(models.User).filter(models.User.id == id)

    if not user_info.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"User with id no. {id} not found!")

    return user_info.first()