from fastapi import APIRouter, Form, Request, Depends, BackgroundTasks
from backend.services.twilio_service import twilio_service
from backend.services.agent_router import route_and_process

router = APIRouter()

async def process_message(form_data: dict):
    """
    Background task to process the incoming message and reply.
    """
    from_number = form_data.get("From")
    body = form_data.get("Body", "")
    num_media = int(form_data.get("NumMedia", 0))
    
    print(f"Processing message from {from_number}. Text: {body}. Media: {num_media}")
    
    image_url = None
    if num_media > 0:
        image_url = form_data.get("MediaUrl0")
            
    # Delegate to router
    response_text = await route_and_process(body, image_url, user_id=from_number)
        
    # Send reply
    twilio_service.send_whatsapp_message(from_number, response_text)

@router.post("/webhook")
async def whatsapp_webhook(
    background_tasks: BackgroundTasks,
    request: Request
):
    """
    Twilio Webhook endpoint.
    """
    form_data = await request.form()
    # Convert ImmutableMultiDict to dict for passing to background task
    data_dict = dict(form_data)
    
    # Basic validation
    if data_dict.get("From"):
        background_tasks.add_task(process_message, data_dict)
    
    return {"status": "received"}
