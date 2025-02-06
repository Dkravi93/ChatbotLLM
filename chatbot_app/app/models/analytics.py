from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database.connection import Base
from datetime import datetime

class Analytics(Base):
    __tablename__ = "analytics"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(String)
    user_id = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
