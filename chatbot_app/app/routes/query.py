from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.schemas.query import Query
from app.services.query_service import process_query

router = APIRouter()

@router.post("/query")
async def handle_query(user_query: Query, db: AsyncSession = Depends(get_db)):
    """Handle user queries and return responses."""
    try:
        response = await process_query(user_query.query, db)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
