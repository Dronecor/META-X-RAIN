"""
Market Intelligence Agent
Uses SerpAPI to provide market insights, competitor analysis, and trend forecasting.
"""
from typing import Dict, Any, List
from backend.services.serpapi_service import serpapi_service
from backend.llm.groq_client import get_groq_client
import logging

logger = logging.getLogger(__name__)


class MarketIntelligenceAgent:
    """
    AI Agent specialized in market intelligence and competitive analysis.
    Uses SerpAPI for web scouting and Groq for intelligent insights.
    """
    
    def __init__(self):
        self.name = "Market Intelligence Agent"
        self.role = "market_intelligence"
        self.serpapi = serpapi_service
        self.llm = get_groq_client(temperature=0.7)
    
    def _get_ai_response(self, prompt: str) -> str:
        """Helper method to get AI response using LangChain"""
        try:
            messages = [
                {"role": "system", "content": self.get_system_prompt()},
                {"role": "user", "content": prompt}
            ]
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            logger.error(f"AI response error: {str(e)}")
            return f"Error getting AI response: {str(e)}"
    
    def get_system_prompt(self) -> str:
        """System prompt for the Market Intelligence Agent"""
        return """You are a Market Intelligence Agent for a fashion retail business.

Your responsibilities:
1. Analyze market trends and consumer behavior
2. Monitor competitor pricing and positioning
3. Identify emerging fashion trends
4. Provide data-driven business recommendations
5. Scout the web for relevant market intelligence

You have access to real-time web data through SerpAPI. Use this to provide:
- Competitive pricing insights
- Market trend analysis
- Competitor positioning
- Product opportunity identification
- News and industry updates

Always provide actionable insights backed by data. Be concise but comprehensive.
Format your responses in a business-friendly manner with clear recommendations."""
    
    async def analyze_market_opportunity(
        self, 
        product_category: str,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Analyze market opportunity for a product category
        
        Args:
            product_category: Category to analyze (e.g., "summer dresses")
            context: Additional context (customer data, inventory, etc.)
            
        Returns:
            Market analysis with trends, competitors, and recommendations
        """
        try:
            # Get market trends
            trends = self.serpapi.get_market_trends(
                category=product_category,
                timeframe="today 3-m"
            )
            
            # Search for products in this category
            products = self.serpapi.search_products(
                query=f"trending {product_category} 2024",
                num_results=20
            )
            
            # Get recent news
            news = self.serpapi.search_news(
                query=f"{product_category} fashion trends",
                num_results=5
            )
            
            # Compile data for AI analysis
            data_summary = f"""
Market Data for {product_category}:

TRENDS:
{trends}

PRODUCT LANDSCAPE:
Found {products.get('total_results', 0)} trending products
Price range: Analyze from product data

RECENT NEWS:
{len(news.get('articles', []))} recent articles found

Context: {context if context else 'No additional context'}
"""
            
            # Get AI insights
            prompt = f"""Analyze this market data and provide actionable insights:

{data_summary}

Provide:
1. Market trend summary (2-3 sentences)
2. Competitive landscape overview
3. Pricing insights
4. Top 3 actionable recommendations
5. Risk factors to consider

Be specific and data-driven."""
            
            ai_response = self._get_ai_response(prompt)
            
            return {
                "category": product_category,
                "analysis": ai_response,
                "raw_data": {
                    "trends": trends,
                    "products": products,
                    "news": news
                },
                "agent": self.name
            }
            
        except Exception as e:
            logger.error(f"Market analysis error: {str(e)}")
            return {
                "error": str(e),
                "agent": self.name
            }
    
    async def analyze_competitor(
        self, 
        competitor_name: str,
        our_brand: str = "Our Brand"
    ) -> Dict[str, Any]:
        """
        Analyze a specific competitor
        
        Args:
            competitor_name: Name of competitor to analyze
            our_brand: Our brand name for comparison
            
        Returns:
            Competitor analysis with positioning and recommendations
        """
        try:
            # Get competitor data
            competitor_data = self.serpapi.analyze_competitors(
                brand_name=competitor_name,
                category="fashion retail"
            )
            
            # Search for competitor products
            products = self.serpapi.search_products(
                query=f"{competitor_name} products",
                num_results=15
            )
            
            # Compile for AI analysis
            data_summary = f"""
Competitor Analysis: {competitor_name}

MARKET PRESENCE:
{competitor_data}

PRODUCT OFFERINGS:
{products.get('total_results', 0)} products found

Compare with: {our_brand}
"""
            
            prompt = f"""Analyze this competitor and provide strategic insights:

{data_summary}

Provide:
1. Competitor positioning summary
2. Their strengths and weaknesses
3. Pricing strategy analysis
4. How we can differentiate from them
5. Specific opportunities to capture their market share

Be strategic and actionable."""
            
            ai_response = self._get_ai_response(prompt)
            
            return {
                "competitor": competitor_name,
                "analysis": ai_response,
                "raw_data": {
                    "competitor_info": competitor_data,
                    "products": products
                },
                "agent": self.name
            }
            
        except Exception as e:
            logger.error(f"Competitor analysis error: {str(e)}")
            return {
                "error": str(e),
                "agent": self.name
            }
    
    async def get_pricing_recommendation(
        self, 
        product_name: str,
        our_cost: float = None
    ) -> Dict[str, Any]:
        """
        Get pricing recommendations based on market data
        
        Args:
            product_name: Product to price
            our_cost: Our cost to produce/source (optional)
            
        Returns:
            Pricing recommendation with competitive analysis
        """
        try:
            # Get price insights
            price_data = self.serpapi.get_price_insights(product_name)
            
            # Get AI recommendation
            data_summary = f"""
Pricing Analysis for: {product_name}

MARKET PRICING:
{price_data}

Our Cost: ${our_cost if our_cost else 'Not provided'}
"""
            
            prompt = f"""Provide pricing recommendations:

{data_summary}

Provide:
1. Recommended retail price with justification
2. Competitive positioning (premium/mid/value)
3. Pricing strategy (penetration/skimming/competitive)
4. Expected margin analysis (if cost provided)
5. Promotional pricing suggestions

Be specific with numbers."""
            
            ai_response = self._get_ai_response(prompt)
            
            return {
                "product": product_name,
                "recommendation": ai_response,
                "market_data": price_data,
                "agent": self.name
            }
            
        except Exception as e:
            logger.error(f"Pricing recommendation error: {str(e)}")
            return {
                "error": str(e),
                "agent": self.name
            }
    
    async def scout_trends(
        self, 
        timeframe: str = "now 7-d"
    ) -> Dict[str, Any]:
        """
        Scout latest fashion trends
        
        Args:
            timeframe: Time period to analyze
            
        Returns:
            Trend report with recommendations
        """
        try:
            # Get fashion trends
            trends = self.serpapi.get_market_trends(
                category="fashion trends",
                timeframe=timeframe
            )
            
            # Get news
            news = self.serpapi.search_news(
                query="fashion trends 2024",
                num_results=10
            )
            
            data_summary = f"""
Fashion Trend Scout Report

SEARCH TRENDS:
{trends}

INDUSTRY NEWS:
{len(news.get('articles', []))} recent articles
{news}
"""
            
            prompt = f"""Analyze these fashion trends and provide insights:

{data_summary}

Provide:
1. Top 3 emerging trends
2. Consumer behavior insights
3. Product opportunities
4. Marketing angle recommendations
5. Timeline for capitalizing on trends

Be trend-forward and actionable."""
            
            ai_response = self._get_ai_response(prompt)
            
            return {
                "timeframe": timeframe,
                "insights": ai_response,
                "raw_data": {
                    "trends": trends,
                    "news": news
                },
                "agent": self.name
            }
            
        except Exception as e:
            logger.error(f"Trend scouting error: {str(e)}")
            return {
                "error": str(e),
                "agent": self.name
            }


# Singleton instance
market_intelligence_agent = MarketIntelligenceAgent()
