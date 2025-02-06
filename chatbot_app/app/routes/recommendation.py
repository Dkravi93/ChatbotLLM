from fastapi import APIRouter, Depends
from app.services.recommendation import recommend_products
from app.database.connection import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.get("/recommendations")
async def get_recommendations(query: str, db: AsyncSession = Depends(get_db)):
    """Get product recommendations based on user query"""
    recommended_products = await recommend_products(query, db)
    return {"recommended_products": recommended_products}
