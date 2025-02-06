from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.database.connection import get_db
from app.utils.auth import hash_password, verify_password, create_access_token
import logging
import traceback

router = APIRouter()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/register")
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        logger.info(f"Registering user {user.username}... {user.email}")

        # Check if the username or email already exists
        stmt = select(User).filter((User.username == user.username) | (User.email == user.email))
        result = await db.execute(stmt)

        # Retrieve the first matching user, if any
        logger.info(f"Existing user: {result}")
        existing_user = result.scalars().first()

        # Log the retrieved user for debugging purposes

        if existing_user:
            raise HTTPException(status_code=400, detail="Username or email already registered.")

        # Hash the password
        hashed_password = hash_password(user.password)

        # Create new user object
        new_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password
        )

        # Add user to the database
        db.add(new_user)
        await db.commit()  # Commit the transaction to the database

        # Refresh the user to get the ID
        await db.refresh(new_user)

        return {"msg": "User registered successfully"}

    except SQLAlchemyError as e:
        # Rollback if there is an error
        await db.rollback()
        logger.error(f"An error occurred while registering the user: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"An error occurred while registering the user: {str(e)}")

@router.post("/login")
async def login_user(user: UserLogin, db: AsyncSession = Depends(get_db)):
    # Check if user exists
    result = await db.execute(select(User).filter(User.username == user.username))
    db_user = result.scalars().first()

    if db_user is None or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Generate JWT token
    token = create_access_token(data={"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}
