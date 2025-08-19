# API Router initialization
from fastapi import APIRouter
from .collections import router as collections_router
from .chat import router as chat_router

# Create main API router
api_router = APIRouter()

# Include all sub-routers
api_router.include_router(collections_router)
api_router.include_router(chat_router)
