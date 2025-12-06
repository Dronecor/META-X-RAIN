from typing import List, Dict, Any

class MarketIntelligenceService:
    def __init__(self):
        pass

    def search_competitor_prices(self, product_name: str) -> List[Dict[str, Any]]:
        """
        Searches the web (SerpAPI / Google Shopping) for similar products and prices.
        """
        print(f"[MOCK] Web Search for prices: {product_name}")
        return [
            {"store": "FashionNova", "price": 35.00, "url": "http://..."},
            {"store": "Zara", "price": 49.90, "url": "http://..."}
        ]

market_service = MarketIntelligenceService()
