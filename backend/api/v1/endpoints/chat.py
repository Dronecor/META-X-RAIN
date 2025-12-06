from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.agent_router import route_and_process

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    image_url: str | None = None
    user_id: str | None = "guest"
    user_name: str | None = None
    email: str | None = None

class ChatResponse(BaseModel):
    response: str

@router.post("/message", response_model=ChatResponse)
async def chat_message(request: ChatRequest):
    """
    Direct chat endpoint for Web UI.
    Same logic as WhatsApp, but synchronous response.
    """
    try:
        user_details = {"full_name": request.user_name, "email": request.email}
        response_text = await route_and_process(
            request.message, 
            request.image_url, 
            user_id=request.user_id or "guest",
            user_details=user_details
        )
        return ChatResponse(response=response_text)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Agent Error: {str(e)}")
