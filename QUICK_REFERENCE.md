# Quick Reference Card - SerpAPI & Vercel

## 🔑 API Keys Needed

```bash
SERPAPI_API_KEY=your_key_here          # Get at: serpapi.com
GROQ_API_KEY=gsk_xxxxx                 # Get at: console.groq.com
TWILIO_ACCOUNT_SID=ACxxxxx             # Get at: twilio.com
TWILIO_AUTH_TOKEN=xxxxx                # Get at: twilio.com
SENDGRID_API_KEY=SG.xxxxx              # Get at: sendgrid.com
PINECONE_API_KEY=xxxxx                 # Get at: pinecone.io
```

---

## 🚀 Quick Commands

### Local Development
```powershell
# Install dependencies
pip install -r backend/requirements.txt

# Start server
python -m uvicorn backend.main:app --reload

# Test market intelligence
python test_market_intelligence.py

# View API docs
# Open: http://localhost:8000/docs
```

### Vercel Deployment
```powershell
# Install CLI
npm install -g vercel

# Login
vercel login

# Deploy to preview
vercel

# Deploy to production
vercel --prod

# View logs
vercel logs --follow
```

---

## 📊 Market Intelligence Endpoints

### Scout Trends
```bash
POST /api/v1/market-intelligence/scout-trends
{
  "timeframe": "now 7-d"  # Options: now 1-d, today 3-m, today 12-m
}
```

### Analyze Market
```bash
POST /api/v1/market-intelligence/analyze-market
{
  "product_category": "summer dresses",
  "context": {"budget": 5000}
}
```

### Competitor Analysis
```bash
POST /api/v1/market-intelligence/analyze-competitor
{
  "competitor_name": "Zara",
  "our_brand": "MyBrand"
}
```

### Pricing Recommendation
```bash
POST /api/v1/market-intelligence/pricing-recommendation
{
  "product_name": "floral dress",
  "our_cost": 25.50
}
```

---

## 🧪 Testing Commands

### Local Testing
```powershell
# Health check
curl http://localhost:8000/health

# Scout trends
curl -X POST http://localhost:8000/api/v1/market-intelligence/scout-trends `
  -H "Content-Type: application/json" `
  -d '{\"timeframe\": \"now 7-d\"}'

# Analyze market
curl -X POST http://localhost:8000/api/v1/market-intelligence/analyze-market `
  -H "Content-Type: application/json" `
  -d '{\"product_category\": \"fashion\", \"context\": {}}'
```

### Production Testing
```powershell
# Replace YOUR-APP with your Vercel URL
curl https://YOUR-APP.vercel.app/health

curl -X POST https://YOUR-APP.vercel.app/api/v1/market-intelligence/scout-trends `
  -H "Content-Type: application/json" `
  -d '{\"timeframe\": \"now 7-d\"}'
```

---

## 📁 Important Files

### Configuration
- `.env` - Environment variables (DO NOT COMMIT)
- `.env.example` - Template for environment variables
- `vercel.json` - Vercel deployment config
- `.vercelignore` - Files to exclude from deployment

### Code
- `backend/services/serpapi_service.py` - SerpAPI wrapper
- `backend/agents/market_intelligence_agent.py` - Market Intelligence AI
- `backend/api/v1/endpoints/market_intelligence.py` - API endpoints
- `backend/main.py` - FastAPI app with Vercel handler

### Documentation
- `SETUP_GUIDE.md` - Complete setup walkthrough
- `SERPAPI_GUIDE.md` - SerpAPI usage guide
- `VERCEL_DEPLOYMENT.md` - Deployment guide
- `OPTIMIZATION_SUMMARY.md` - What was changed

### Testing
- `test_market_intelligence.py` - Test script

---

## 🔧 Environment Variables

### Required for SerpAPI
```bash
SERPAPI_API_KEY=your_serpapi_key_here
```

### Required for Vercel
```bash
VERCEL_ENV=production
VERCEL_URL=your-app.vercel.app
```

### Database
```bash
# Local (SQLite)
DATABASE_URL=sqlite:///./agentic_crm.db

# Production (PostgreSQL)
DATABASE_URL=postgresql://user:password@host:5432/database?sslmode=require
```

---

## 💰 Cost Tracking

### Free Tiers
- **Vercel Hobby**: 100GB bandwidth, 100 hours execution
- **SerpAPI**: 100 searches/month
- **Groq**: Check console.groq.com for limits

### Monitor Usage
- Vercel: https://vercel.com/dashboard/usage
- SerpAPI: https://serpapi.com/dashboard
- Groq: https://console.groq.com/usage

---

## 🐛 Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| "SERPAPI_API_KEY not set" | Add to `.env` or Vercel env vars |
| Vercel build fails | Check `vercel logs [url]` |
| Database connection fails | Verify `DATABASE_URL` format |
| Function timeout | Optimize code or upgrade to Pro |
| Rate limit exceeded | Implement caching or upgrade plan |

---

## 📚 Documentation Links

- **API Docs**: http://localhost:8000/docs (local)
- **SerpAPI**: https://serpapi.com/docs
- **Vercel**: https://vercel.com/docs
- **FastAPI**: https://fastapi.tiangolo.com/

---

## 🎯 Timeframe Options

For trend analysis:
- `"now 1-H"` - Last hour
- `"now 1-d"` - Last day
- `"now 7-d"` - Last 7 days
- `"today 1-m"` - Last month
- `"today 3-m"` - Last 3 months
- `"today 12-m"` - Last year

---

## 🔄 Deployment Workflow

1. **Develop Locally**
   ```powershell
   python -m uvicorn backend.main:app --reload
   ```

2. **Test Changes**
   ```powershell
   python test_market_intelligence.py
   ```

3. **Commit to Git**
   ```powershell
   git add .
   git commit -m "Your changes"
   git push
   ```

4. **Auto-Deploy**
   - Vercel automatically deploys on push to main
   - Preview deployments for other branches

---

## 📞 Support

- **GitHub Issues**: For bug reports
- **SerpAPI Support**: support@serpapi.com
- **Vercel Support**: support@vercel.com
- **Groq Discord**: Check console.groq.com

---

## ✅ Pre-Deployment Checklist

- [ ] All API keys added to `.env`
- [ ] Dependencies installed (`pip install -r backend/requirements.txt`)
- [ ] Local testing passed (`python test_market_intelligence.py`)
- [ ] API endpoints tested (`curl http://localhost:8000/health`)
- [ ] Vercel CLI installed (`npm install -g vercel`)
- [ ] Logged into Vercel (`vercel login`)
- [ ] Environment variables added to Vercel dashboard
- [ ] Database configured (PostgreSQL for production)
- [ ] Deployed to production (`vercel --prod`)
- [ ] Production endpoints tested
- [ ] WhatsApp webhook updated (if using)
- [ ] Monitoring enabled
- [ ] Custom domain configured (optional)

---

**📌 Keep this card handy for quick reference!**
