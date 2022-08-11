from fastapi import APIRouter

router = APIRouter(
    tags = ['Authentication'],
    prefix="/login"
)

@router.get("/")
def login():
    return 'login'