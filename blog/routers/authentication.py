from fastapi import APIRouter, status, HTTPException, Depends
from .. import schemas, database, models
from sqlalchemy.orm import Session
from ..hashing import Hash

router = APIRouter(
    tags = ['Authentication'],
    prefix="/login"
)

@router.post("/", status_code=status.HTTP_202_ACCEPTED)
def login(request: schemas.Login, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with username = {request.username} not found!")

    if not Hash.verify(request.password , user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Given password is not correct!")

    # Generate JWT token here and RETURN it

    return user