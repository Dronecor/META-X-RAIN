# Complete Setup Guide - SerpAPI & Vercel Optimization

This guide will help you set up your Agentic AI CRM with SerpAPI for web scouting and deploy it to Vercel.

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Setup](#local-setup)
3. [SerpAPI Configuration](#serpapi-configuration)
4. [Testing Locally](#testing-locally)
5. [Vercel Deployment](#vercel-deployment)
6. [Post-Deployment](#post-deployment)

---

## Prerequisites

### Required Accounts
- ✅ **SerpAPI Account**: [Sign up here](https://serpapi.com/)
- ✅ **Vercel Account**: [Sign up here](https://vercel.com/)
- ✅ **Groq API Key**: [Get here](https://console.groq.com/)
- ✅ **Twilio Account**: [Sign up here](https://www.twilio.com/)
- ✅ **SendGrid Account**: [Sign up here](https://sendgrid.com/)
- ✅ **Pinecone Account**: [Sign up here](https://www.pinecone.io/)

### Required Software
- Python 3.9+
- Node.js 18+ (for Vercel CLI)
- Git
- PowerShell (Windows) or Bash (Mac/Linux)

---

## Local Setup

### Step 1: Clone and Navigate
```powershell
cd "c:\Users\USER\OneDrive\Documents\META hackathon"
```

### Step 2: Install Python Dependencies
```powershell
pip install -r backend/requirements.txt
```

This will install:
- FastAPI & Uvicorn
- SQLAlchemy & Database drivers
- LangChain & Groq
- Twilio & SendGrid
- **google-search-results** (SerpAPI SDK)
- **mangum** (Vercel/AWS Lambda adapter)
- And more...

### Step 3: Configure Environment Variables

Copy the example file:
```powershell
cp .env.example .env
```

Edit `.env` and add your API keys:

```bash
# Project config
PROJECT_NAME="Agentic AI CRM"
SECRET_KEY=your_secret_key_here_generate_a_random_string

# Database (SQLite for local, PostgreSQL for production)
DATABASE_URL=sqlite:///./agentic_crm.db

# Groq / AI
GROQ_API_KEY=gsk_your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile

# Messaging
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Email
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Vector DB
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENV=us-east-1

# SerpAPI (NEW - REQUIRED for Market Intelligence)
SERPAPI_API_KEY=your_serpapi_key_here

# Admin
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=change_this_secure_password

# Vercel (will be auto-set in production)
VERCEL_ENV=development
VERCEL_URL=localhost:8000
```

---

## SerpAPI Configuration

### Step 1: Get Your API Key

1. Go to [https://serpapi.com/](https://serpapi.com/)
2. Sign up for a free account
3. Navigate to Dashboard → API Key
4. Copy your API key

**Free Tier Includes:**
- 100 searches/month
- All search engines
- No credit card required

### Step 2: Add to Environment

Add to your `.env` file:
```bash
SERPAPI_API_KEY=your_actual_serpapi_key_here
```

### Step 3: Verify Installation

Test the SerpAPI service:
```powershell
python test_market_intelligence.py
```

You should see:
- ✅ SerpAPI key found
- 📊 Trend insights
- 📈 Market analysis
- 💰 Pricing recommendations

---

## Testing Locally

### Step 1: Start the Backend

```powershell
python -m uvicorn backend.main:app --reload
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### Step 2: Test Health Endpoint

Open a new terminal:
```powershell
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "environment": "local"
}
```

### Step 3: Test Market Intelligence API

#### Scout Trends
```powershell
curl -X POST http://localhost:8000/api/v1/market-intelligence/scout-trends `
  -H "Content-Type: application/json" `
  -d '{\"timeframe\": \"now 7-d\"}'
```

#### Analyze Market
```powershell
curl -X POST http://localhost:8000/api/v1/market-intelligence/analyze-market `
  -H "Content-Type: application/json" `
  -d '{\"product_category\": \"summer dresses\", \"context\": {\"budget\": 5000}}'
```

#### Get Pricing Recommendation
```powershell
curl -X POST http://localhost:8000/api/v1/market-intelligence/pricing-recommendation `
  -H "Content-Type: application/json" `
  -d '{\"product_name\": \"floral dress\", \"our_cost\": 25.50}'
```

#### Analyze Competitor
```powershell
curl -X POST http://localhost:8000/api/v1/market-intelligence/analyze-competitor `
  -H "Content-Type: application/json" `
  -d '{\"competitor_name\": \"Zara\", \"our_brand\": \"MyBrand\"}'
```

### Step 4: View API Documentation

Open in browser:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Vercel Deployment

### Step 1: Install Vercel CLI

```powershell
npm install -g vercel
```

### Step 2: Login to Vercel

```powershell
vercel login
```

Follow the prompts to authenticate.

### Step 3: Deploy

```powershell
cd "c:\Users\USER\OneDrive\Documents\META hackathon"
vercel
```

Answer the prompts:
- **Set up and deploy**: Yes
- **Which scope**: Your account
- **Link to existing project**: No
- **Project name**: agentic-ai-crm (or your choice)
- **Directory**: ./ (current directory)
- **Override settings**: No

### Step 4: Configure Environment Variables

#### Option A: Via Dashboard (Recommended)

1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Select your project
3. Go to Settings → Environment Variables
4. Add each variable from your `.env` file:

```
PROJECT_NAME = Agentic AI CRM
SECRET_KEY = [generate secure key]
DATABASE_URL = [PostgreSQL connection string]
GROQ_API_KEY = [your key]
GROQ_MODEL = llama-3.3-70b-versatile
TWILIO_ACCOUNT_SID = [your SID]
TWILIO_AUTH_TOKEN = [your token]
TWILIO_WHATSAPP_NUMBER = whatsapp:+14155238886
SENDGRID_API_KEY = [your key]
PINECONE_API_KEY = [your key]
PINECONE_ENV = us-east-1
SERPAPI_API_KEY = [your key]
ADMIN_EMAIL = admin@example.com
ADMIN_PASSWORD = [secure password]
```

#### Option B: Via CLI

```powershell
vercel env add GROQ_API_KEY
# Enter value when prompted

vercel env add SERPAPI_API_KEY
# Enter value when prompted

# Repeat for all variables...
```

### Step 5: Set Up Database

#### Option 1: Vercel Postgres (Recommended)

```powershell
vercel postgres create
```

This will automatically set `POSTGRES_URL` in your environment.

#### Option 2: External Database

Use Neon, Supabase, or Railway:

1. Create a PostgreSQL database
2. Get the connection string
3. Add to Vercel environment variables:
   ```
   DATABASE_URL = postgresql://user:password@host:5432/database?sslmode=require
   ```

### Step 6: Deploy to Production

```powershell
vercel --prod
```

You'll get a production URL like:
```
https://agentic-ai-crm.vercel.app
```

### Step 7: Verify Deployment

Test your production API:
```powershell
curl https://your-app.vercel.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "environment": "production"
}
```

---

## Post-Deployment

### 1. Update WhatsApp Webhook

In Twilio Console:
1. Go to WhatsApp Sandbox Settings
2. Update webhook URL to:
   ```
   https://your-app.vercel.app/api/v1/whatsapp/webhook
   ```

### 2. Set Up Custom Domain (Optional)

1. Go to Vercel Dashboard → Your Project → Settings → Domains
2. Add your custom domain
3. Follow DNS configuration instructions

### 3. Monitor Performance

- **Vercel Analytics**: https://vercel.com/dashboard/analytics
- **Function Logs**: https://vercel.com/dashboard/[project]/logs
- **SerpAPI Usage**: https://serpapi.com/dashboard

### 4. Set Up Alerts

#### Vercel Alerts
- Go to Project Settings → Alerts
- Enable deployment failure notifications
- Set up performance alerts

#### SerpAPI Alerts
- Go to SerpAPI Dashboard
- Set usage threshold alerts (e.g., 80% of monthly quota)

### 5. Enable CI/CD

If using GitHub:
1. Install Vercel GitHub App
2. Connect your repository
3. Every push to `main` → Production deployment
4. Every PR → Preview deployment

---

## Optimization Tips

### 1. Reduce Cold Starts

Add to `backend/main.py`:
```python
@app.on_event("startup")
async def startup_event():
    # Pre-initialize services
    from backend.services.serpapi_service import serpapi_service
    logger.info("Services initialized")
```

### 2. Implement Caching

Cache SerpAPI results to reduce API calls:
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_search(query: str):
    return serpapi_service.search_products(query)
```

### 3. Rate Limiting

Add rate limiting to protect your API:
```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@app.get("/api/endpoint")
@limiter.limit("10/minute")
async def endpoint():
    return {"message": "Rate limited"}
```

### 4. Monitor Costs

- **Vercel**: Free tier → 100GB bandwidth, 100 hours execution
- **SerpAPI**: Free tier → 100 searches/month
- **Groq**: Check your usage at console.groq.com

---

## Troubleshooting

### Issue: "SERPAPI_API_KEY not set"
**Solution**: 
1. Check `.env` file has the key
2. For Vercel, check environment variables in dashboard
3. Redeploy after adding variables

### Issue: Vercel deployment fails
**Solution**:
1. Check build logs: `vercel logs [deployment-url]`
2. Verify `requirements.txt` is correct
3. Ensure `vercel.json` is in root directory

### Issue: Database connection fails
**Solution**:
1. Verify `DATABASE_URL` format
2. Ensure SSL mode is enabled for production
3. Check database allows connections from Vercel IPs

### Issue: Function timeout
**Solution**:
1. Optimize code to run faster
2. Reduce `num_results` in SerpAPI calls
3. Upgrade to Vercel Pro for 60s timeout

---

## Next Steps

1. ✅ **Test all endpoints** locally
2. ✅ **Deploy to Vercel**
3. ✅ **Configure webhooks**
4. ✅ **Set up monitoring**
5. ✅ **Implement caching**
6. ✅ **Add rate limiting**
7. ✅ **Set up custom domain**
8. ✅ **Enable analytics**

---

## Resources

### Documentation
- [SerpAPI Guide](SERPAPI_GUIDE.md)
- [Vercel Deployment](VERCEL_DEPLOYMENT.md)
- [Architecture](ARCHITECTURE.md)
- [API Documentation](http://localhost:8000/docs)

### External Links
- [SerpAPI Docs](https://serpapi.com/docs)
- [Vercel Docs](https://vercel.com/docs)
- [Groq API](https://console.groq.com/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)

### Support
- GitHub Issues: For bug reports
- SerpAPI Support: support@serpapi.com
- Vercel Support: support@vercel.com

---

## Quick Reference

### Local Development
```powershell
# Start backend
python -m uvicorn backend.main:app --reload

# Test market intelligence
python test_market_intelligence.py

# View API docs
# Open: http://localhost:8000/docs
```

### Deployment
```powershell
# Deploy to preview
vercel

# Deploy to production
vercel --prod

# View logs
vercel logs --follow
```

### Environment Variables
```powershell
# Add variable
vercel env add VARIABLE_NAME

# Pull variables locally
vercel env pull

# List variables
vercel env ls
```

---

**🎉 Congratulations!** Your Agentic AI CRM is now optimized for SerpAPI web scouting and ready for Vercel deployment!
