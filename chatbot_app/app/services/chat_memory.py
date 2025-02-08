from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.models.chat_history import ChatHistory
from app.schemas.chat_history import ChatHistoryCreate
import traceback

class ChatMemory:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def store_query(self, chat: ChatHistoryCreate):
        """Store the user query and chatbot response in the database."""
        new_entry = ChatHistory(**chat.dict())
        self.db.add(new_entry)
        await self.db.commit()

    async def get_recent_queries(self, user_id: int, limit: int = 5):
        """Retrieve the last `limit` queries from the user."""
        try:
            result = await self.db.execute(
                select(ChatHistory)  # Corrected: Query the ChatHistory model
                .where(ChatHistory.user_id == user_id)
                .order_by(ChatHistory.timestamp.desc())
                .limit(limit)
            )

            queries = result.scalars().all()  # Simplified result handling

            if not queries:
                return ["No recent queries found for this user."]  # Handle empty history case

            return queries
        except SQLAlchemyError as e:
            print(traceback.format_exc())
            return [f"Error retrieving recent queries. Please try again. Error: {str(e)}"]

