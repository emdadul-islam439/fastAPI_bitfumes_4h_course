from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status
from ..hashing import Hash

def create_user(request: schemas.User, db: Session):
    new_user = models.User(name = request.name, email = request.email, password = Hash.get_password_hash(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user(id: int, db: Session):
    user_info = db.query(models.User).filter(models.User.id == id)

    if not user_info.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"User with id no. {id} not found!")

    return user_info.first()
    