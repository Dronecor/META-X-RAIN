from fastapi import APIRouter
from pydantic import BaseModel
from backend.services.agent_router import route_and_process

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    image_url: str | None = None
    user_id: str | None = "guest"

class ChatResponse(BaseModel):
    response: str

@router.post("/message", response_model=ChatResponse)
async def chat_message(request: ChatRequest):
    """
    Direct chat endpoint for Web UI.
    Same logic as WhatsApp, but synchronous response.
    """
    response_text = await route_and_process(request.message, request.image_url)
    return ChatResponse(response=response_text)
