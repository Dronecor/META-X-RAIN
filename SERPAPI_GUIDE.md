# SerpAPI Integration Guide

## Overview
This project uses **SerpAPI** for web scouting and market intelligence. SerpAPI provides real-time access to Google Search results, Google Shopping, Google Trends, and more.

## Features

### 1. **Product Search**
Search for products across the web with pricing and availability:
```python
from backend.services.serpapi_service import serpapi_service

results = serpapi_service.search_products(
    query="trending summer dresses 2024",
    location="United States",
    num_results=20
)
```

### 2. **Competitor Analysis**
Analyze competitors and their market presence:
```python
competitor_data = serpapi_service.analyze_competitors(
    brand_name="Zara",
    category="fashion retail"
)
```

### 3. **Market Trends**
Get trending topics and search interest over time:
```python
trends = serpapi_service.get_market_trends(
    category="fashion",
    timeframe="today 3-m"
)
```

### 4. **News Search**
Find recent news articles about fashion and retail:
```python
news = serpapi_service.search_news(
    query="fashion trends 2024",
    num_results=10
)
```

### 5. **Price Insights**
Compare prices across different retailers:
```python
price_data = serpapi_service.get_price_insights(
    product_name="floral summer dress"
)
```

## API Endpoints

### Market Analysis
```bash
POST /api/v1/market-intelligence/analyze-market
Content-Type: application/json

{
  "product_category": "summer dresses",
  "context": {
    "current_inventory": 50,
    "target_audience": "women 25-40"
  }
}
```

### Competitor Analysis
```bash
POST /api/v1/market-intelligence/analyze-competitor
Content-Type: application/json

{
  "competitor_name": "Zara",
  "our_brand": "MyFashionBrand"
}
```

### Pricing Recommendations
```bash
POST /api/v1/market-intelligence/pricing-recommendation
Content-Type: application/json

{
  "product_name": "floral summer dress",
  "our_cost": 25.50
}
```

### Trend Scouting
```bash
POST /api/v1/market-intelligence/scout-trends
Content-Type: application/json

{
  "timeframe": "today 3-m"
}
```

## Setup

### 1. Get SerpAPI Key
1. Sign up at [https://serpapi.com/](https://serpapi.com/)
2. Get your API key from the dashboard
3. Free tier includes 100 searches/month

### 2. Add to Environment
Update your `.env` file:
```bash
SERPAPI_API_KEY=your_serpapi_key_here
```

### 3. Install Dependencies
```bash
pip install google-search-results
```

## Usage Examples

### Example 1: Market Opportunity Analysis
```python
from backend.agents.market_intelligence_agent import market_intelligence_agent

# Analyze market for a new product category
result = await market_intelligence_agent.analyze_market_opportunity(
    product_category="sustainable fashion",
    context={
        "budget": 10000,
        "target_market": "eco-conscious millennials"
    }
)

print(result["analysis"])  # AI-generated insights
print(result["raw_data"]["trends"])  # Raw trend data
```

### Example 2: Competitive Pricing
```python
# Get pricing recommendations
result = await market_intelligence_agent.get_pricing_recommendation(
    product_name="organic cotton t-shirt",
    our_cost=12.50
)

print(result["recommendation"])  # AI pricing strategy
print(result["market_data"]["price_range"])  # Market price range
```

### Example 3: Trend Forecasting
```python
# Scout latest trends
result = await market_intelligence_agent.scout_trends(
    timeframe="now 7-d"
)

print(result["insights"])  # AI trend analysis
print(result["raw_data"]["news"])  # Recent news articles
```

## Best Practices

### 1. **Rate Limiting**
- Free tier: 100 searches/month
- Paid tier: Up to 5,000 searches/month
- Cache results when possible
- Use appropriate timeframes for trends

### 2. **Query Optimization**
```python
# Good: Specific and targeted
query = "women's summer dresses under $50 2024"

# Bad: Too broad
query = "clothes"
```

### 3. **Error Handling**
```python
try:
    results = serpapi_service.search_products(query="...")
    if "error" in results:
        # Handle API error
        logger.error(f"SerpAPI error: {results['error']}")
except Exception as e:
    # Handle exception
    logger.error(f"Unexpected error: {str(e)}")
```

### 4. **Cost Management**
- Monitor API usage in SerpAPI dashboard
- Set up usage alerts
- Cache frequently requested data
- Use batch processing for multiple queries

## Timeframe Options

For trend analysis, use these timeframe formats:

- `"now 1-H"` - Last hour
- `"now 4-H"` - Last 4 hours
- `"now 1-d"` - Last day
- `"now 7-d"` - Last 7 days
- `"today 1-m"` - Last month
- `"today 3-m"` - Last 3 months
- `"today 12-m"` - Last year
- `"today 5-y"` - Last 5 years

## Supported Search Engines

SerpAPI supports multiple search engines:
- Google Search
- Google Shopping
- Google Trends
- Google News
- Bing
- Yahoo
- Baidu
- Yandex

## Advanced Features

### Custom Location Targeting
```python
results = serpapi_service.search_products(
    query="winter coats",
    location="New York, NY, United States"
)
```

### Language Targeting
Modify the service to add language parameter:
```python
params = {
    "engine": "google_shopping",
    "q": query,
    "location": location,
    "hl": "en",  # Language
    "gl": "us",  # Country
    "api_key": self.api_key
}
```

## Troubleshooting

### Issue: "SERPAPI_API_KEY not set"
**Solution**: Add your API key to `.env` file

### Issue: Rate limit exceeded
**Solution**: Upgrade plan or implement caching

### Issue: No results returned
**Solution**: Check query specificity and location settings

### Issue: Slow response times
**Solution**: Reduce `num_results` parameter or use caching

## Resources

- [SerpAPI Documentation](https://serpapi.com/docs)
- [SerpAPI Playground](https://serpapi.com/playground)
- [Pricing Plans](https://serpapi.com/pricing)
- [API Status](https://status.serpapi.com/)

## Integration with Other Agents

The Market Intelligence Agent can be used by other agents:

```python
# Sales Agent using market intelligence
from backend.agents.market_intelligence_agent import market_intelligence_agent

async def recommend_products(customer_preferences):
    # Get market trends
    trends = await market_intelligence_agent.scout_trends()
    
    # Use trends to recommend products
    # ...
```

## Monitoring and Analytics

Track SerpAPI usage:
1. Dashboard: https://serpapi.com/dashboard
2. API calls remaining
3. Monthly usage statistics
4. Response time metrics

## Security

- Never commit API keys to Git
- Use environment variables
- Rotate keys periodically
- Monitor for unauthorized usage
- Set up billing alerts
