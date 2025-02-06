from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.query import router as query_router
from app.routes.user import router as user_router
from app.routes.analytics import router as analytics_router
from app.routes.recommendation import router as recommendation_router
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

origins = ["http://localhost:5173", "http://127.0.0.1:55256"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(user_router, prefix="/api/users", tags=["users"])

# Include query routes
app.include_router(query_router, prefix="/api", tags=["queries"])
app.include_router(analytics_router, prefix="/api", tags=["analytics"])

# Include recommendation routes
app.include_router(recommendation_router, prefix="/api", tags=["recommendations"])