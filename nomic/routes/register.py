from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from nomic.database import crud
from nomic.utils.security import hash_password

router = APIRouter()


@router.post("/register")
async def register_user(
    username: str, password: str, db: Session = Depends(crud.get_db)
):
    hashed_password = hash_password(password)
    try:
        user = crud.create_user(db, username, hashed_password)
        return {"message": "User registered successfully", "user_id": user.id}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
