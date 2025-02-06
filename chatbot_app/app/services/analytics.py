from app.models.analytics import Analytics
from app.database.connection import get_db
from sqlalchemy.ext.asyncio import AsyncSession

async def track_query(query: str, user_id: int, db: AsyncSession):
    """Store user query for analytics."""
    analytics_entry = Analytics(query=query, user_id=user_id)
    db.add(analytics_entry)
    await db.commit()
