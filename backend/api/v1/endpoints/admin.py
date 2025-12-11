from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from backend.database import get_db
from backend.models import Conversation, Message, User, Order

router = APIRouter()

@router.get("/conversations")
def get_conversations(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """
    Get all conversations with summaries for the admin dashboard.
    """
    conversations = db.query(Conversation).order_by(Conversation.last_message_at.desc()).offset(skip).limit(limit).all()
    
    results = []
    for conv in conversations:
        # Get customer details
        customer = db.query(User).filter(User.id == conv.customer_id).first()
        customer_name = customer.full_name if customer else "Unknown"
        customer_contact = customer.phone_number or customer.email or "N/A"
        
        results.append({
            "id": conv.id,
            "customer": f"{customer_name} ({customer_contact})",
            "platform": conv.platform,
            "summary": conv.summary or "No summary available yet.",
            "last_active": conv.last_message_at,
            "link": f"/conversations/{conv.id}" # For frontend routing if needed
        })
    
    return results

@router.get("/conversations/{conversation_id}")
def get_conversation_details(conversation_id: int, db: Session = Depends(get_db)):
    """
    Get messages for a specific conversation.
    """
    conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
        
    messages = db.query(Message).filter(Message.conversation_id == conv.id).order_by(Message.timestamp.asc()).all()
    
    return {
        "id": conv.id,
        "summary": conv.summary,
        "messages": [
            {
                "sender": m.sender,
                "content": m.content,
                "timestamp": m.timestamp
            } for m in messages
        ]
    }

@router.get("/orders")
def get_orders(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """
    Get all orders for admin verification.
    """
    orders = db.query(models.Order).order_by(models.Order.created_at.desc()).offset(skip).limit(limit).all()
    return orders

@router.post("/orders/{order_id}/verify")
def verify_order(order_id: int, status: str, db: Session = Depends(get_db)):
    """
    Update order status (e.g. to 'paid', 'shipped', 'cancelled').
    """
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.status = status
    db.commit()
    db.refresh(order)
    return order
