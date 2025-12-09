# 🚀 Deployment Checklist

Use this checklist to ensure a smooth deployment of your Agentic AI CRM with SerpAPI and Vercel.

---

## Phase 1: Prerequisites ✅

### Accounts Setup
- [ ] **SerpAPI Account** created at [serpapi.com](https://serpapi.com/)
  - [ ] API key obtained (free tier: 100 searches/month)
  - [ ] Billing alerts configured (optional)

- [ ] **Vercel Account** created at [vercel.com](https://vercel.com/)
  - [ ] GitHub/GitLab connected (for CI/CD)
  - [ ] Payment method added (if using Pro features)

- [ ] **Groq Account** created at [console.groq.com](https://console.groq.com/)
  - [ ] API key obtained
  - [ ] Usage limits understood

- [ ] **Database Provider** selected
  - [ ] Option A: Vercel Postgres
  - [ ] Option B: Neon/Supabase/Railway
  - [ ] Connection string obtained

- [ ] **Twilio Account** (for WhatsApp)
  - [ ] Account SID obtained
  - [ ] Auth Token obtained
  - [ ] WhatsApp sandbox configured

- [ ] **SendGrid Account** (for emails)
  - [ ] API key obtained
  - [ ] Sender email verified

- [ ] **Pinecone Account** (for vector search)
  - [ ] API key obtained
  - [ ] Environment/region selected

### Software Installation
- [ ] **Python 3.9+** installed
  - [ ] Verify: `python --version`

- [ ] **Node.js 18+** installed
  - [ ] Verify: `node --version`

- [ ] **Git** installed
  - [ ] Verify: `git --version`

- [ ] **Vercel CLI** installed
  - [ ] Run: `npm install -g vercel`
  - [ ] Verify: `vercel --version`

---

## Phase 2: Local Setup ✅

### Project Setup
- [ ] Navigate to project directory
  ```powershell
  cd "c:\Users\USER\OneDrive\Documents\META hackathon"
  ```

- [ ] Install Python dependencies
  ```powershell
  pip install -r backend/requirements.txt
  ```

- [ ] Verify new packages installed
  - [ ] `google-search-results` (SerpAPI)
  - [ ] `mangum` (Vercel adapter)

### Environment Configuration
- [ ] Copy `.env.example` to `.env`
  ```powershell
  cp .env.example .env
  ```

- [ ] Fill in all environment variables in `.env`:
  - [ ] `PROJECT_NAME`
  - [ ] `SECRET_KEY` (generate secure random string)
  - [ ] `DATABASE_URL` (SQLite for local)
  - [ ] `GROQ_API_KEY`
  - [ ] `GROQ_MODEL`
  - [ ] `TWILIO_ACCOUNT_SID`
  - [ ] `TWILIO_AUTH_TOKEN`
  - [ ] `TWILIO_WHATSAPP_NUMBER`
  - [ ] `SENDGRID_API_KEY`
  - [ ] `PINECONE_API_KEY`
  - [ ] `PINECONE_ENV`
  - [ ] `SERPAPI_API_KEY` ⭐ NEW
  - [ ] `ADMIN_EMAIL`
  - [ ] `ADMIN_PASSWORD`

- [ ] Verify `.env` file is in `.gitignore`

---

## Phase 3: Local Testing ✅

### Backend Testing
- [ ] Start backend server
  ```powershell
  python -m uvicorn backend.main:app --reload
  ```

- [ ] Verify server started successfully
  - [ ] Check console for "Application startup complete"
  - [ ] No error messages

- [ ] Test health endpoint
  ```powershell
  curl http://localhost:8000/health
  ```
  - [ ] Response: `{"status": "healthy", "database": "connected"}`

- [ ] Test root endpoint
  ```powershell
  curl http://localhost:8000/
  ```
  - [ ] Response includes project name and version

- [ ] Access API documentation
  - [ ] Open: http://localhost:8000/docs
  - [ ] Verify all endpoints visible
  - [ ] Check Market Intelligence endpoints present

### Market Intelligence Testing
- [ ] Run test script
  ```powershell
  python test_market_intelligence.py
  ```

- [ ] Verify test results:
  - [ ] SerpAPI key detected
  - [ ] Trend scouting works
  - [ ] Market analysis works
  - [ ] Pricing recommendation works
  - [ ] No errors

- [ ] Test individual endpoints:

  - [ ] **Scout Trends**
    ```powershell
    curl -X POST http://localhost:8000/api/v1/market-intelligence/scout-trends `
      -H "Content-Type: application/json" `
      -d '{\"timeframe\": \"now 7-d\"}'
    ```

  - [ ] **Analyze Market**
    ```powershell
    curl -X POST http://localhost:8000/api/v1/market-intelligence/analyze-market `
      -H "Content-Type: application/json" `
      -d '{\"product_category\": \"fashion\", \"context\": {}}'
    ```

  - [ ] **Pricing Recommendation**
    ```powershell
    curl -X POST http://localhost:8000/api/v1/market-intelligence/pricing-recommendation `
      -H "Content-Type: application/json" `
      -d '{\"product_name\": \"dress\", \"our_cost\": 25.0}'
    ```

  - [ ] **Competitor Analysis**
    ```powershell
    curl -X POST http://localhost:8000/api/v1/market-intelligence/analyze-competitor `
      -H "Content-Type: application/json" `
      -d '{\"competitor_name\": \"Zara\", \"our_brand\": \"MyBrand\"}'
    ```

### Existing Features Testing
- [ ] Test WhatsApp endpoint (if configured)
- [ ] Test chat endpoint
- [ ] Test admin endpoints
- [ ] Test visual search (if configured)

---

## Phase 4: Vercel Preparation ✅

### Code Review
- [ ] Review `vercel.json` configuration
  - [ ] Correct build settings
  - [ ] Proper routes configured
  - [ ] Function memory and timeout set

- [ ] Review `.vercelignore`
  - [ ] Excludes unnecessary files
  - [ ] Database files excluded
  - [ ] `.env` excluded

- [ ] Verify Git repository
  - [ ] All changes committed
  - [ ] `.env` NOT in repository
  - [ ] `.gitignore` properly configured

### Database Setup
- [ ] Choose database option:
  
  **Option A: Vercel Postgres**
  - [ ] Run: `vercel postgres create`
  - [ ] Note the connection string
  
  **Option B: External Provider**
  - [ ] Create PostgreSQL database
  - [ ] Get connection string
  - [ ] Test connection locally
  - [ ] Ensure SSL mode enabled

- [ ] Update `DATABASE_URL` for production
  - [ ] Format: `postgresql://user:password@host:5432/database?sslmode=require`

---

## Phase 5: Vercel Deployment ✅

### Initial Deployment
- [ ] Login to Vercel
  ```powershell
  vercel login
  ```

- [ ] Deploy to preview
  ```powershell
  vercel
  ```

- [ ] Answer prompts:
  - [ ] Set up and deploy: **Yes**
  - [ ] Scope: **Your account**
  - [ ] Link to existing project: **No**
  - [ ] Project name: **agentic-ai-crm** (or your choice)
  - [ ] Directory: **./**
  - [ ] Override settings: **No**

- [ ] Note preview URL provided

### Environment Variables Configuration

**Via Vercel Dashboard (Recommended):**
- [ ] Go to [vercel.com/dashboard](https://vercel.com/dashboard)
- [ ] Select your project
- [ ] Navigate to Settings → Environment Variables
- [ ] Add each variable:

  **Project Config:**
  - [ ] `PROJECT_NAME` = Agentic AI CRM
  - [ ] `SECRET_KEY` = [generate secure key]

  **Database:**
  - [ ] `DATABASE_URL` = [PostgreSQL connection string]

  **AI & ML:**
  - [ ] `GROQ_API_KEY` = [your key]
  - [ ] `GROQ_MODEL` = llama-3.3-70b-versatile

  **Messaging:**
  - [ ] `TWILIO_ACCOUNT_SID` = [your SID]
  - [ ] `TWILIO_AUTH_TOKEN` = [your token]
  - [ ] `TWILIO_WHATSAPP_NUMBER` = whatsapp:+14155238886

  **Email:**
  - [ ] `SENDGRID_API_KEY` = [your key]

  **Vector DB:**
  - [ ] `PINECONE_API_KEY` = [your key]
  - [ ] `PINECONE_ENV` = us-east-1

  **Web Scouting (NEW):**
  - [ ] `SERPAPI_API_KEY` = [your key] ⭐

  **Admin:**
  - [ ] `ADMIN_EMAIL` = admin@example.com
  - [ ] `ADMIN_PASSWORD` = [secure password]

- [ ] Set environment for each variable:
  - [ ] Production
  - [ ] Preview (optional)
  - [ ] Development (optional)

### Production Deployment
- [ ] Deploy to production
  ```powershell
  vercel --prod
  ```

- [ ] Note production URL
  - [ ] Format: `https://your-app.vercel.app`

- [ ] Wait for deployment to complete
  - [ ] Check build logs
  - [ ] Verify no errors

---

## Phase 6: Post-Deployment Testing ✅

### Production API Testing
- [ ] Test health endpoint
  ```powershell
  curl https://your-app.vercel.app/health
  ```
  - [ ] Response: `{"status": "healthy", "database": "connected", "environment": "production"}`

- [ ] Test root endpoint
  ```powershell
  curl https://your-app.vercel.app/
  ```
  - [ ] Verify environment is "production"

- [ ] Test Market Intelligence endpoints:

  - [ ] Scout Trends
    ```powershell
    curl -X POST https://your-app.vercel.app/api/v1/market-intelligence/scout-trends `
      -H "Content-Type: application/json" `
      -d '{\"timeframe\": \"now 7-d\"}'
    ```

  - [ ] Analyze Market
  - [ ] Pricing Recommendation
  - [ ] Competitor Analysis

- [ ] Access API documentation
  - [ ] Open: https://your-app.vercel.app/docs
  - [ ] Verify all endpoints work

### Integration Testing
- [ ] Test WhatsApp integration
  - [ ] Update Twilio webhook URL
  - [ ] URL: `https://your-app.vercel.app/api/v1/whatsapp/webhook`
  - [ ] Send test message
  - [ ] Verify response

- [ ] Test email notifications (if configured)

- [ ] Test all AI agents
  - [ ] Sales Agent
  - [ ] Support Agent
  - [ ] Visual Search Agent
  - [ ] Market Intelligence Agent ⭐

---

## Phase 7: Monitoring & Optimization ✅

### Monitoring Setup
- [ ] Enable Vercel Analytics
  - [ ] Go to Project → Analytics
  - [ ] Review performance metrics

- [ ] Set up alerts
  - [ ] Deployment failures
  - [ ] Performance degradation
  - [ ] Error rate threshold

- [ ] Monitor SerpAPI usage
  - [ ] Go to [serpapi.com/dashboard](https://serpapi.com/dashboard)
  - [ ] Check monthly quota
  - [ ] Set up usage alerts

- [ ] Monitor Groq usage
  - [ ] Go to [console.groq.com](https://console.groq.com/)
  - [ ] Check API usage
  - [ ] Review rate limits

### Performance Optimization
- [ ] Review function execution times
  - [ ] Check Vercel dashboard
  - [ ] Identify slow endpoints

- [ ] Implement caching (if needed)
  - [ ] Cache SerpAPI results
  - [ ] Cache AI responses (where appropriate)

- [ ] Optimize cold starts
  - [ ] Review initialization code
  - [ ] Pre-load critical services

### Security Hardening
- [ ] Review CORS settings
  - [ ] Verify allowed origins
  - [ ] Test cross-origin requests

- [ ] Implement rate limiting
  - [ ] Add to critical endpoints
  - [ ] Test limits

- [ ] Review environment variables
  - [ ] Ensure no secrets in code
  - [ ] Rotate sensitive keys

---

## Phase 8: Documentation & Handoff ✅

### Documentation Review
- [ ] Review all documentation files:
  - [ ] README.md
  - [ ] SETUP_GUIDE.md
  - [ ] SERPAPI_GUIDE.md
  - [ ] VERCEL_DEPLOYMENT.md
  - [ ] OPTIMIZATION_SUMMARY.md
  - [ ] QUICK_REFERENCE.md

- [ ] Update with production URLs
- [ ] Add any custom configurations
- [ ] Document any issues encountered

### Team Handoff (if applicable)
- [ ] Share production URL
- [ ] Share Vercel dashboard access
- [ ] Share API documentation
- [ ] Share monitoring dashboards
- [ ] Document deployment process
- [ ] Train team on new features

---

## Phase 9: Optional Enhancements ✅

### Custom Domain
- [ ] Purchase domain (if needed)
- [ ] Add domain in Vercel
  - [ ] Go to Settings → Domains
  - [ ] Add custom domain
  - [ ] Configure DNS records

- [ ] Verify domain
- [ ] Update CORS for new domain
- [ ] Update webhooks with new domain

### CI/CD Setup
- [ ] Connect GitHub repository
  - [ ] Install Vercel GitHub App
  - [ ] Configure auto-deployments

- [ ] Set up branch deployments
  - [ ] `main` → Production
  - [ ] `develop` → Preview
  - [ ] Feature branches → Preview

- [ ] Configure deployment protection
  - [ ] Require approvals (optional)
  - [ ] Run tests before deploy (optional)

### Advanced Features
- [ ] Implement advanced caching
- [ ] Add request logging
- [ ] Set up error tracking (e.g., Sentry)
- [ ] Implement A/B testing
- [ ] Add performance monitoring

---

## Phase 10: Go Live! 🎉

### Final Checks
- [ ] All tests passing
- [ ] All integrations working
- [ ] Monitoring enabled
- [ ] Documentation complete
- [ ] Team trained (if applicable)

### Launch
- [ ] Announce to stakeholders
- [ ] Monitor initial traffic
- [ ] Be ready for support requests
- [ ] Collect feedback

### Post-Launch
- [ ] Monitor for 24-48 hours
- [ ] Review logs for errors
- [ ] Check performance metrics
- [ ] Optimize based on real usage
- [ ] Plan next iteration

---

## 📊 Success Metrics

Track these metrics post-deployment:

### Technical Metrics
- [ ] API response time < 2s
- [ ] Error rate < 1%
- [ ] Uptime > 99.9%
- [ ] Cold start time < 3s

### Business Metrics
- [ ] SerpAPI usage within quota
- [ ] Groq API usage within limits
- [ ] Database performance acceptable
- [ ] User satisfaction high

### Cost Metrics
- [ ] Vercel costs within budget
- [ ] API costs within budget
- [ ] Database costs within budget

---

## 🆘 Rollback Plan

If something goes wrong:

1. **Immediate Rollback**
   ```powershell
   vercel rollback
   ```

2. **Via Dashboard**
   - Go to Deployments
   - Find previous working deployment
   - Click "Promote to Production"

3. **Investigate Issues**
   - Check logs: `vercel logs [deployment-url]`
   - Review error messages
   - Check environment variables

4. **Fix and Redeploy**
   - Fix issues locally
   - Test thoroughly
   - Deploy again

---

## ✅ Completion

**Congratulations!** 🎉

You have successfully:
- ✅ Set up SerpAPI for web scouting
- ✅ Deployed to Vercel
- ✅ Configured all services
- ✅ Tested all endpoints
- ✅ Set up monitoring
- ✅ Launched to production

**Your Agentic AI CRM is now live!**

---

**Next Steps:**
1. Monitor performance
2. Collect user feedback
3. Iterate and improve
4. Scale as needed

**Need Help?**
- Review: [SETUP_GUIDE.md](SETUP_GUIDE.md)
- Reference: [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- Support: GitHub Issues or contact support
