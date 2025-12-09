"""
SerpAPI Service for Web Scouting
Provides market intelligence, competitor analysis, and product trend research.
"""
from typing import Dict, List, Optional, Any
from serpapi import GoogleSearch
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class SerpAPIService:
    """Service for web scouting using SerpAPI"""
    
    def __init__(self):
        self.api_key = os.getenv("SERPAPI_API_KEY")
        if not self.api_key:
            logger.warning("SERPAPI_API_KEY not set. Web scouting features will be disabled.")
    
    def search_products(
        self, 
        query: str, 
        location: str = "United States",
        num_results: int = 10
    ) -> Dict[str, Any]:
        """
        Search for products across the web
        
        Args:
            query: Search query (e.g., "trending summer dresses 2024")
            location: Geographic location for search
            num_results: Number of results to return
            
        Returns:
            Dictionary containing search results with products, prices, and sources
        """
        if not self.api_key:
            return {"error": "SerpAPI key not configured"}
        
        try:
            params = {
                "engine": "google_shopping",
                "q": query,
                "location": location,
                "num": num_results,
                "api_key": self.api_key
            }
            
            search = GoogleSearch(params)
            results = search.get_dict()
            
            # Extract shopping results
            shopping_results = results.get("shopping_results", [])
            
            products = []
            for item in shopping_results:
                products.append({
                    "title": item.get("title"),
                    "price": item.get("price"),
                    "source": item.get("source"),
                    "link": item.get("link"),
                    "thumbnail": item.get("thumbnail"),
                    "rating": item.get("rating"),
                    "reviews": item.get("reviews"),
                    "delivery": item.get("delivery")
                })
            
            return {
                "query": query,
                "location": location,
                "timestamp": datetime.utcnow().isoformat(),
                "total_results": len(products),
                "products": products
            }
            
        except Exception as e:
            logger.error(f"SerpAPI search error: {str(e)}")
            return {"error": str(e)}
    
    def analyze_competitors(
        self, 
        brand_name: str, 
        category: str = "fashion retail"
    ) -> Dict[str, Any]:
        """
        Analyze competitors in the market
        
        Args:
            brand_name: Your brand name
            category: Product category
            
        Returns:
            Competitor analysis with pricing, positioning, and market presence
        """
        if not self.api_key:
            return {"error": "SerpAPI key not configured"}
        
        try:
            # Search for competitors
            query = f"{category} brands like {brand_name}"
            params = {
                "engine": "google",
                "q": query,
                "num": 20,
                "api_key": self.api_key
            }
            
            search = GoogleSearch(params)
            results = search.get_dict()
            
            organic_results = results.get("organic_results", [])
            
            competitors = []
            for result in organic_results[:10]:
                competitors.append({
                    "title": result.get("title"),
                    "link": result.get("link"),
                    "snippet": result.get("snippet"),
                    "position": result.get("position")
                })
            
            return {
                "brand": brand_name,
                "category": category,
                "timestamp": datetime.utcnow().isoformat(),
                "competitors_found": len(competitors),
                "competitors": competitors
            }
            
        except Exception as e:
            logger.error(f"Competitor analysis error: {str(e)}")
            return {"error": str(e)}
    
    def get_market_trends(
        self, 
        category: str = "fashion",
        timeframe: str = "now 7-d"
    ) -> Dict[str, Any]:
        """
        Get market trends and insights
        
        Args:
            category: Product category
            timeframe: Google Trends timeframe (e.g., "now 7-d", "today 3-m")
            
        Returns:
            Trending topics, search interest, and related queries
        """
        if not self.api_key:
            return {"error": "SerpAPI key not configured"}
        
        try:
            params = {
                "engine": "google_trends",
                "q": category,
                "data_type": "TIMESERIES",
                "date": timeframe,
                "api_key": self.api_key
            }
            
            search = GoogleSearch(params)
            results = search.get_dict()
            
            # Extract interest over time
            interest_over_time = results.get("interest_over_time", {})
            timeline_data = interest_over_time.get("timeline_data", [])
            
            # Get related queries
            related_queries = results.get("related_queries", {})
            
            return {
                "category": category,
                "timeframe": timeframe,
                "timestamp": datetime.utcnow().isoformat(),
                "interest_timeline": timeline_data,
                "related_queries": related_queries
            }
            
        except Exception as e:
            logger.error(f"Market trends error: {str(e)}")
            return {"error": str(e)}
    
    def search_news(
        self, 
        query: str, 
        num_results: int = 10
    ) -> Dict[str, Any]:
        """
        Search for news articles related to fashion/retail
        
        Args:
            query: Search query
            num_results: Number of news articles to return
            
        Returns:
            Recent news articles with titles, snippets, and sources
        """
        if not self.api_key:
            return {"error": "SerpAPI key not configured"}
        
        try:
            params = {
                "engine": "google",
                "q": query,
                "tbm": "nws",  # News search
                "num": num_results,
                "api_key": self.api_key
            }
            
            search = GoogleSearch(params)
            results = search.get_dict()
            
            news_results = results.get("news_results", [])
            
            articles = []
            for article in news_results:
                articles.append({
                    "title": article.get("title"),
                    "link": article.get("link"),
                    "snippet": article.get("snippet"),
                    "source": article.get("source"),
                    "date": article.get("date"),
                    "thumbnail": article.get("thumbnail")
                })
            
            return {
                "query": query,
                "timestamp": datetime.utcnow().isoformat(),
                "total_articles": len(articles),
                "articles": articles
            }
            
        except Exception as e:
            logger.error(f"News search error: {str(e)}")
            return {"error": str(e)}
    
    def get_price_insights(
        self, 
        product_name: str
    ) -> Dict[str, Any]:
        """
        Get pricing insights for a product across different retailers
        
        Args:
            product_name: Name of the product
            
        Returns:
            Price comparison across retailers with min, max, and average prices
        """
        if not self.api_key:
            return {"error": "SerpAPI key not configured"}
        
        try:
            params = {
                "engine": "google_shopping",
                "q": product_name,
                "num": 50,
                "api_key": self.api_key
            }
            
            search = GoogleSearch(params)
            results = search.get_dict()
            
            shopping_results = results.get("shopping_results", [])
            
            prices = []
            retailers = {}
            
            for item in shopping_results:
                price_str = item.get("price", "")
                source = item.get("source", "Unknown")
                
                # Extract numeric price
                try:
                    # Remove currency symbols and convert to float
                    price_clean = ''.join(c for c in price_str if c.isdigit() or c == '.')
                    if price_clean:
                        price = float(price_clean)
                        prices.append(price)
                        
                        if source not in retailers:
                            retailers[source] = []
                        retailers[source].append(price)
                except:
                    continue
            
            if prices:
                return {
                    "product": product_name,
                    "timestamp": datetime.utcnow().isoformat(),
                    "price_range": {
                        "min": min(prices),
                        "max": max(prices),
                        "average": sum(prices) / len(prices),
                        "median": sorted(prices)[len(prices) // 2]
                    },
                    "total_listings": len(prices),
                    "retailers": {k: {
                        "count": len(v),
                        "avg_price": sum(v) / len(v)
                    } for k, v in retailers.items()}
                }
            else:
                return {
                    "product": product_name,
                    "error": "No pricing data found"
                }
            
        except Exception as e:
            logger.error(f"Price insights error: {str(e)}")
            return {"error": str(e)}


# Singleton instance
serpapi_service = SerpAPIService()
