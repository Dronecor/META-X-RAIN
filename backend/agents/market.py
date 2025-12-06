from backend.agents.base import BaseAgent
from backend.services.market_intelligence import market_service

MARKET_SYSTEM_PROMPT = """
You are a Market Intelligence Expert.
Your primary role is to assist the Business Admin by providing insights on competitor pricing and trends.
When asked about a product's market standing, you search the web for current prices of similar items.
"""

class MarketIntelligenceAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="MarketIntelligenceAgent",
            role="Competitor Analysis",
            system_prompt=MARKET_SYSTEM_PROMPT
        )
    
    async def analyze_price(self, product_name: str) -> str:
        competitors = market_service.search_competitor_prices(product_name)
        
        # Format for LLM
        comp_str = "\n".join([f"- {c['store']}: ${c['price']}" for c in competitors])
        
        context = {
            "Product": product_name,
            "Competitor Data": comp_str
        }
        
        return await self.run(f"Analyze the market price for {product_name}", context=context)
