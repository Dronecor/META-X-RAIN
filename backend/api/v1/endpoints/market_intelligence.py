"""
Market Intelligence API Endpoints
Provides market analysis, competitor insights, and trend forecasting.
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any
from backend.agents.market_intelligence_agent import market_intelligence_agent
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/market-intelligence", tags=["Market Intelligence"])


class MarketAnalysisRequest(BaseModel):
    """Request model for market analysis"""
    product_category: str
    context: Optional[Dict[str, Any]] = None


class CompetitorAnalysisRequest(BaseModel):
    """Request model for competitor analysis"""
    competitor_name: str
    our_brand: Optional[str] = "Our Brand"


class PricingRequest(BaseModel):
    """Request model for pricing recommendations"""
    product_name: str
    our_cost: Optional[float] = None


class TrendScoutRequest(BaseModel):
    """Request model for trend scouting"""
    timeframe: Optional[str] = "now 7-d"


@router.post("/analyze-market")
async def analyze_market(request: MarketAnalysisRequest):
    """
    Analyze market opportunity for a product category
    
    Example:
    ```json
    {
        "product_category": "summer dresses",
        "context": {
            "current_inventory": 50,
            "target_audience": "women 25-40"
        }
    }
    ```
    """
    try:
        result = await market_intelligence_agent.analyze_market_opportunity(
            product_category=request.product_category,
            context=request.context
        )
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
    
    except Exception as e:
        logger.error(f"Market analysis endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-competitor")
async def analyze_competitor(request: CompetitorAnalysisRequest):
    """
    Analyze a specific competitor
    
    Example:
    ```json
    {
        "competitor_name": "Zara",
        "our_brand": "MyFashionBrand"
    }
    ```
    """
    try:
        result = await market_intelligence_agent.analyze_competitor(
            competitor_name=request.competitor_name,
            our_brand=request.our_brand
        )
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
    
    except Exception as e:
        logger.error(f"Competitor analysis endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/pricing-recommendation")
async def get_pricing_recommendation(request: PricingRequest):
    """
    Get pricing recommendations based on market data
    
    Example:
    ```json
    {
        "product_name": "floral summer dress",
        "our_cost": 25.50
    }
    ```
    """
    try:
        result = await market_intelligence_agent.get_pricing_recommendation(
            product_name=request.product_name,
            our_cost=request.our_cost
        )
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
    
    except Exception as e:
        logger.error(f"Pricing recommendation endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/scout-trends")
async def scout_trends(request: TrendScoutRequest):
    """
    Scout latest fashion trends
    
    Example:
    ```json
    {
        "timeframe": "today 3-m"
    }
    ```
    
    Timeframe options:
    - "now 7-d" (last 7 days)
    - "today 3-m" (last 3 months)
    - "today 12-m" (last year)
    """
    try:
        result = await market_intelligence_agent.scout_trends(
            timeframe=request.timeframe
        )
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
    
    except Exception as e:
        logger.error(f"Trend scouting endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint for market intelligence service"""
    return {
        "status": "healthy",
        "service": "Market Intelligence API",
        "agent": market_intelligence_agent.name
    }
