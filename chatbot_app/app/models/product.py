from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from app.database.connection import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand = Column(String)
    price = Column(Float)
    category = Column(String)
    description = Column(Text)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
