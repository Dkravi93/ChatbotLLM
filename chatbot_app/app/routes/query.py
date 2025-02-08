from app.schemas.chat_history import ChatHistoryCreate
from app.services.chat_memory import ChatMemory
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.schemas.query import Query
from app.services.query_service import process_query
from app.utils.auth import get_current_user
from app.models.user import User
from cachetools import TTLCache
from app.utils.auth import verify_token
from sqlalchemy.future import select
import logging

router = APIRouter()
user_cache = TTLCache(maxsize=1000, ttl=300)
logger = logging.getLogger(__name__)

@router.post("/query")
async def handle_query(user_query: Query, db: AsyncSession = Depends(get_db)):
    """Handle user queries, store chat history, and return responses."""
    try:
        username = verify_token(user_query.token)
        db_user = await db.execute(select(User).filter(User.username == username))
        user = db_user.scalars().first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        response = await process_query(user.id, user_query.query, db, chat_memory=ChatMemory)
        # ✅ Store chat history
        chat_memory = ChatMemory(db)
        chat_entry = ChatHistoryCreate(
            user_id=user.id,
            query=user_query.query,
            response=response
        )
        await chat_memory.store_query(chat_entry)

        return {"response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
