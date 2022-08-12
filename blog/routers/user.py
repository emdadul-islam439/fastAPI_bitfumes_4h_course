from fastapi import APIRouter, status, Depends
from .. import schemas, database, oauth2
from sqlalchemy.orm import Session
from ..repository import user

router = APIRouter(
    tags=["Users"],
    prefix="/user"
)
get_db = database.get_db

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return user.create_user(request, db)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model= schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return user.get_user(id, db)