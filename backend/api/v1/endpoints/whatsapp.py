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
            
    # Implement Opt-in Logic
    from backend.database import SessionLocal
    from backend.models import User
    
    db = SessionLocal()
    try:
        # Check if user exists
        user = db.query(User).filter(User.phone_number == from_number).first()
        
        if not user:
            # Create new user
            user = User(phone_number=from_number, role="customer", bot_opt_in=False)
            db.add(user)
            db.commit()
            db.refresh(user)
            
        if not user.bot_opt_in:
            # Check if message is a confirmation
            if body.strip().upper() in ["YES", "Y", "START"]:
                user.bot_opt_in = True
                db.commit()
                response_text = "Great! You are now connected to the ShopBuddy AI Assistant. How can I help you today?"
            else:
                response_text = "Hello! Would you like to speak with our AI assistant for faster responses? Reply YES to connect."
                # We skip routing to agents until they opt-in
                twilio_service.send_whatsapp_message(from_number, response_text)
                return

    except Exception as e:
        print(f"Error in WhatsApp Opt-in: {e}")
        # Fallback to allowing access or just logging error
    finally:
        db.close()

    # If opted in, delegate to router
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
