from sqlalchemy.orm import Session
from backend.models import Conversation, Message, User
from backend.database import SessionLocal
from backend.llm.groq_client import get_groq_client
from langchain_core.messages import SystemMessage, HumanMessage

class ChatHistoryService:
    def __init__(self):
        self.llm = get_groq_client(model="llama-3.3-70b-versatile")

    def get_db(self):
        return SessionLocal()

    def get_or_create_user(self, db: Session, identifier: str, full_name: str = None, email: str = None) -> User:
        # Check if int (ID) or str (Phone/Email)
        user = db.query(User).filter(User.phone_number == identifier).first()
        if not user:
            # Try email if phone failed or wasn't provided (assuming identifier could be either)
            user = db.query(User).filter(User.email == identifier).first()
        
        if not user:
            # Create new user
            email_val = email or f"{identifier}@example.com"
            user = User(
                full_name=full_name or "Guest", 
                phone_number=identifier, 
                email=email_val
            )
            db.add(user)
        else:
            # Update existing user info if provided
            if full_name:
                user.full_name = full_name
            if email:
                user.email = email
                
        db.commit()
        db.refresh(user)
        return user

    def get_or_create_conversation(self, db: Session, user_id: int, platform: str = "general") -> Conversation:
        # Find active conversation? Or just the last one?
        # Let's get the most recent one.
        conv = db.query(Conversation).filter(
            Conversation.customer_id == user_id,
            Conversation.platform == platform
        ).order_by(Conversation.last_message_at.desc()).first()

        if not conv:
            conv = Conversation(customer_id=user_id, platform=platform)
            db.add(conv)
            db.commit()
            db.refresh(conv)
        return conv

    def add_message(self, db: Session, conversation_id: int, sender: str, content: str):
        msg = Message(
            conversation_id=conversation_id,
            sender=sender,
            content=content
        )
        db.add(msg)
        
        # Update conversation timestamp
        conv = db.query(Conversation).get(conversation_id)
        conv.last_message_at = func.now() # handled by server_default but good to be explicit if using onupdate
        
        db.commit()

    def get_context(self, identifier: str, full_name: str = None, email: str = None) -> dict:
        """
        Retrieves the summary and recent messages for a user.
        Can optionally update user details.
        """
        db = self.get_db()
        try:
            user = self.get_or_create_user(db, identifier, full_name, email)
            conv = self.get_or_create_conversation(db, user.id)
            
            # Fetch summary
            summary = conv.summary or ""
            
            # Fetch recent messages (last 10)
            messages = db.query(Message).filter(
                Message.conversation_id == conv.id
            ).order_by(Message.timestamp.desc()).limit(10).all()
            
            # They are in reverse order (newest first), flip them for context
            history_msgs = []
            for m in reversed(messages):
                history_msgs.append({"sender": m.sender, "content": m.content})
                
            return {
                "conversation_id": conv.id,
                "summary": summary,
                "history": history_msgs
            }
        finally:
            db.close()

    def save_interaction(self, identifier: str, user_msg: str, agent_msg: str):
        db = self.get_db()
        try:
            user = self.get_or_create_user(db, identifier)
            conv = self.get_or_create_conversation(db, user.id)
            
            self.add_message(db, conv.id, "user", user_msg)
            self.add_message(db, conv.id, "agent", agent_msg)
            
            # Check for summarization trigger
            # simple logic: if message count > 10 and no summary in last 5 messages...
            # simplified: Retrieve all messages, if count > 15, summarize first 10.
            
            total_msgs = db.query(Message).filter(Message.conversation_id == conv.id).count()
            if total_msgs > 10:
                self._summarize_updates(db, conv)
                
        finally:
            db.close()

    def _summarize_updates(self, db: Session, conv: Conversation):
        """
        Summarize the conversation to reduce context window.
        """
        # Get current summary
        current_summary = conv.summary or "No summary."
        
        # Get messages to summarize (e.g., all messages except the last 3 to keep recent context fresh)
        # Actually, standard practice is: Summary + Last K Messages. 
        # So we update the summary with the 'middle' messages that are falling out of the window.
        
        # For hackathon simplicity: Just regenerate summary from last 20 messages every time it grows? 
        # No, that's expensive.
        # Let's do: New Summary = LLM(Old Summary + New Recent Messages)
        
        messages = db.query(Message).filter(
            Message.conversation_id == conv.id
        ).order_by(Message.timestamp.asc()).all()
        
        # If we have a lot of messages, let's condense.
        text_to_summarize = f"Current Summary: {current_summary}\n\nRecent Interaction:\n"
        for m in messages[-5:]: # Just take last 5 to verify concept
             text_to_summarize += f"{m.sender}: {m.content}\n"
             
        prompt = f"""
        You are a memory manager for an AI assistant. Update the conversation summary based on the recent interaction.
        Keep important details (user preferences, names, orders, styles). 
        Condensed Summary only.
        
        {text_to_summarize}
        """
        
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            new_summary = response.content
            
            conv.summary = new_summary
            db.commit()
            print(f"[Memory] Updated summary for Conv {conv.id}")
        except Exception as e:
            print(f"[Memory] Failed to summarize: {e}")

from sqlalchemy import func
chat_history = ChatHistoryService()
