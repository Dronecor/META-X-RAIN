from backend.agents.base import BaseAgent
from backend.services.image_search import image_search_service

VISUAL_SEARCH_SYSTEM_PROMPT = """
You are a Visual Search Specialist.
Your goal is to help customers find products that visually match the images they upload.
When a user uploads an image, you analyze it (using provided tools) and suggest similar items from our catalog.
You should describe WHY the items are similar (e.g., "I found this similar floral pattern...", "Here is a jacket in a similar style...").

"""

class VisualSearchAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="VisualSearchAgent",
            role="Visual Product Discovery",
            system_prompt=VISUAL_SEARCH_SYSTEM_PROMPT
        )

    async def run_with_image(self, user_text: str, image_url: str, user_id: str = "guest", user_details: dict = None) -> str:
        """
        Specialized run method for image inputs.
        """
        # 1. Perform image search
        results = image_search_service.search_by_image(image_url)
        
        # 2. Format results for the LLM
        results_str = "\n".join([f"- {item['name']} (${item['price']}) - ImageURL: {item['image_url']}" for item in results])
        
        # 3. Create context
        context = {
            "User Image URL": image_url,
            "Visual Search Results": results_str,
            "Instruction": "You MUST display the product images using Markdown: ![Product Name](ImageURL). Do not just list them."
        }
        
        # 4. Invoke LLM
        response = await self.run(user_text or "Find something like this.", context=context, user_id=user_id, user_details=user_details)
        return response
