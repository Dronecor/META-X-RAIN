"""
Quick test script for Market Intelligence features
Run this to test SerpAPI integration
"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_market_intelligence():
    """Test Market Intelligence Agent"""
    from backend.agents.market_intelligence_agent import market_intelligence_agent
    
    print("=" * 60)
    print("🧪 Testing Market Intelligence Agent")
    print("=" * 60)
    
    # Check if API key is set
    serpapi_key = os.getenv("SERPAPI_API_KEY")
    if not serpapi_key or serpapi_key == "your_serpapi_key_here":
        print("\n⚠️  WARNING: SERPAPI_API_KEY not set!")
        print("Please add your SerpAPI key to .env file")
        print("Get one at: https://serpapi.com/")
        return
    
    print(f"\n✅ SerpAPI key found: {serpapi_key[:10]}...")
    
    # Test 1: Scout Trends
    print("\n" + "=" * 60)
    print("Test 1: Scouting Fashion Trends")
    print("=" * 60)
    
    try:
        result = await market_intelligence_agent.scout_trends(
            timeframe="now 7-d"
        )
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"\n📊 Trend Insights:")
            print(result.get("insights", "No insights available"))
            print(f"\n📰 Found {len(result.get('raw_data', {}).get('news', {}).get('articles', []))} news articles")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 2: Analyze Market
    print("\n" + "=" * 60)
    print("Test 2: Market Opportunity Analysis")
    print("=" * 60)
    
    try:
        result = await market_intelligence_agent.analyze_market_opportunity(
            product_category="sustainable fashion",
            context={"budget": 10000}
        )
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"\n📈 Market Analysis:")
            print(result.get("analysis", "No analysis available"))
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 3: Pricing Recommendation
    print("\n" + "=" * 60)
    print("Test 3: Pricing Recommendation")
    print("=" * 60)
    
    try:
        result = await market_intelligence_agent.get_pricing_recommendation(
            product_name="summer dress",
            our_cost=25.00
        )
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"\n💰 Pricing Recommendation:")
            print(result.get("recommendation", "No recommendation available"))
            
            market_data = result.get("market_data", {})
            price_range = market_data.get("price_range", {})
            if price_range:
                print(f"\n📊 Market Price Range:")
                print(f"  Min: ${price_range.get('min', 'N/A')}")
                print(f"  Max: ${price_range.get('max', 'N/A')}")
                print(f"  Average: ${price_range.get('average', 'N/A'):.2f}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print("\n" + "=" * 60)
    print("✅ Testing Complete!")
    print("=" * 60)


async def test_serpapi_service():
    """Test SerpAPI Service directly"""
    from backend.services.serpapi_service import serpapi_service
    
    print("\n" + "=" * 60)
    print("🔍 Testing SerpAPI Service")
    print("=" * 60)
    
    # Test product search
    print("\nSearching for products...")
    results = serpapi_service.search_products(
        query="trending fashion 2024",
        num_results=5
    )
    
    if "error" in results:
        print(f"❌ Error: {results['error']}")
    else:
        print(f"✅ Found {results.get('total_results', 0)} products")
        for i, product in enumerate(results.get('products', [])[:3], 1):
            print(f"\n  {i}. {product.get('title', 'N/A')}")
            print(f"     Price: {product.get('price', 'N/A')}")
            print(f"     Source: {product.get('source', 'N/A')}")


if __name__ == "__main__":
    print("\n🚀 Market Intelligence Test Suite")
    print("=" * 60)
    
    # Run tests
    asyncio.run(test_market_intelligence())
    
    # Uncomment to test SerpAPI service directly
    # asyncio.run(test_serpapi_service())
