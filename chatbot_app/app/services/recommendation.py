from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product import Product
from app.models.supplier import Supplier
from app.database.connection import get_db

async def recommend_products(query: str, db: AsyncSession):
    """Recommend related products based on category or brand"""
    # Simplified example: matching products based on the category
    result = await db.execute(f"""
        SELECT * FROM products WHERE category ILIKE '%{query}%' LIMIT 5
    """)
    return result.all()
