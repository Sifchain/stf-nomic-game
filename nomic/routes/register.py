import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from nomic.database import crud
from nomic.utils.security import hash_password

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/register")
async def register_user(
    username: str, password: str, db: Session = Depends(crud.get_db)
):
    hashed_password = hash_password(password)
    try:
        user = crud.create_user(db, username, hashed_password)
        return {"message": "User registered successfully", "user_id": user.id}
    except IntegrityError as ie:
        # Log the detailed error for internal use
        logger.error(f"Failed to register user {username}: {str(ie.orig)}")
        db.rollback()  # Roll back the session to ensure consistency
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration failed: Username may already be in use.",
        )
    except Exception as e:
        # Log the unexpected error for internal use
        logger.error(
            f"Unexpected error during registration for user {username}: {str(e)}"
        )
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later.",
        )
