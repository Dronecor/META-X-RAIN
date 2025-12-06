from fastapi import APIRouter
from backend.api.v1.endpoints import whatsapp, chat

api_router = APIRouter()
api_router.include_router(whatsapp.router, prefix="/whatsapp", tags=["whatsapp"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
# api_router.include_router(products.router, prefix="/products", tags=["products"])
