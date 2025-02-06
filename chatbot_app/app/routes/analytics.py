from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.models.analytics import Analytics

router = APIRouter()

@router.get("/analytics")
async def get_analytics(db: AsyncSession = Depends(get_db)):
    """Fetch analytics on user queries."""
    result = await db.execute("SELECT query, COUNT(*) FROM analytics GROUP BY query ORDER BY COUNT(*) DESC LIMIT 10")
    return result.all()
