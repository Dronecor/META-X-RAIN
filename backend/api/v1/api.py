from fastapi import APIRouter
from backend.api.v1.endpoints import whatsapp, chat, admin, market_intelligence, products, upload

api_router = APIRouter()
api_router.include_router(whatsapp.router, prefix="/whatsapp", tags=["whatsapp"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(market_intelligence.router, tags=["market-intelligence"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(upload.router, prefix="/utils", tags=["utils"])

