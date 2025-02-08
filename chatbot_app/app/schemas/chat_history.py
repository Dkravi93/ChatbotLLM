from pydantic import BaseModel
from datetime import datetime

class ChatHistoryBase(BaseModel):
    query: str
    response: str

class ChatHistoryCreate(ChatHistoryBase):
    user_id: int

class ChatHistoryResponse(ChatHistoryBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
