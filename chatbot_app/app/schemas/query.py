from pydantic import BaseModel

class Query(BaseModel):
    token: str
    query: str
