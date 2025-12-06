from backend.agents.sales import SalesAgent
from backend.agents.support import SupportAgent
from backend.agents.visual_search import VisualSearchAgent

# Instantiate agents once (singleton pattern for checking)
sales_agent = SalesAgent()
support_agent = SupportAgent()
visual_search_agent = VisualSearchAgent()

async def route_and_process(text: str, image_url: str = None, user_id: str = "guest", user_details: dict = None) -> str:
    """
    Core routing logic to determine which agent handles the request.
    Returns the agent's response as a string.
    """
    
    # 1. Handle Images (Visual Search)
    if image_url:
        print(f"[Router] Dispatching to VisualSearchAgent. Image: {image_url}")
        return await visual_search_agent.run_with_image(text, image_url, user_id=user_id, user_details=user_details)
    
    # 2. Handle Text Router
    message_lower = text.lower()
    
    # Simple keyword-based routing for V1
    # In V2, we use an LLM RouterAgent
    if any(x in message_lower for x in ["order", "refund", "return", "track", "help", "late"]):
        print(f"[Router] Dispatching to SupportAgent: {text}")
        return await support_agent.run(text, user_id=user_id, user_details=user_details)
    else:
        # Default to sales for broad queries
        print(f"[Router] Dispatching to SalesAgent: {text}")
        return await sales_agent.run(text, user_id=user_id, user_details=user_details)
