# Vercel Deployment Guide

## Overview
This guide covers deploying your Agentic AI CRM to **Vercel** for serverless hosting with automatic scaling and global CDN.

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Vercel CLI**: Install globally
   ```bash
   npm install -g vercel
   ```
3. **Git Repository**: Your code should be in a Git repository (GitHub, GitLab, or Bitbucket)

## Project Structure

Your project is now optimized for Vercel with:
- ✅ `vercel.json` - Deployment configuration
- ✅ `backend/main.py` - FastAPI app with Mangum handler
- ✅ `backend/requirements.txt` - Python dependencies
- ✅ `.env.example` - Environment variable template

## Quick Deploy

### Option 1: Deploy via Vercel Dashboard (Recommended)

1. **Connect Repository**
   - Go to [vercel.com/new](https://vercel.com/new)
   - Import your Git repository
   - Vercel will auto-detect the configuration

2. **Configure Environment Variables**
   Add these in the Vercel dashboard under "Environment Variables":
   ```
   PROJECT_NAME=Agentic AI CRM
   SECRET_KEY=<generate-secure-key>
   DATABASE_URL=<your-database-url>
   GROQ_API_KEY=<your-groq-key>
   GROQ_MODEL=llama-3.3-70b-versatile
   TWILIO_ACCOUNT_SID=<your-twilio-sid>
   TWILIO_AUTH_TOKEN=<your-twilio-token>
   TWILIO_WHATSAPP_NUMBER=whatsapp:+1234567890
   SENDGRID_API_KEY=<your-sendgrid-key>
   PINECONE_API_KEY=<your-pinecone-key>
   PINECONE_ENV=us-east-1
   SERPAPI_API_KEY=<your-serpapi-key>
   ADMIN_EMAIL=admin@example.com
   ADMIN_PASSWORD=<secure-password>
   ```

3. **Deploy**
   - Click "Deploy"
   - Vercel will build and deploy automatically
   - You'll get a production URL like `https://your-app.vercel.app`

### Option 2: Deploy via CLI

1. **Login to Vercel**
   ```bash
   vercel login
   ```

2. **Deploy**
   ```bash
   cd "c:\Users\USER\OneDrive\Documents\META hackathon"
   vercel
   ```

3. **Follow Prompts**
   - Set up and deploy: Yes
   - Which scope: Your account
   - Link to existing project: No
   - Project name: agentic-ai-crm
   - Directory: ./
   - Override settings: No

4. **Set Environment Variables**
   ```bash
   vercel env add GROQ_API_KEY
   vercel env add SERPAPI_API_KEY
   vercel env add DATABASE_URL
   # ... add all other variables
   ```

5. **Deploy to Production**
   ```bash
   vercel --prod
   ```

## Database Setup

### Option 1: Vercel Postgres (Recommended)

1. **Create Database**
   ```bash
   vercel postgres create
   ```

2. **Link to Project**
   ```bash
   vercel link
   vercel env pull
   ```

3. **Update DATABASE_URL**
   Vercel will automatically set `POSTGRES_URL` environment variable

### Option 2: External Database

Use any PostgreSQL provider:
- **Neon**: [neon.tech](https://neon.tech) (Free tier available)
- **Supabase**: [supabase.com](https://supabase.com) (Free tier available)
- **Railway**: [railway.app](https://railway.app)
- **PlanetScale**: [planetscale.com](https://planetscale.com)

Example connection string:
```
DATABASE_URL=postgresql://user:password@host:5432/database?sslmode=require
```

## Configuration Details

### vercel.json Explained

```json
{
  "version": 2,
  "builds": [
    {
      "src": "backend/main.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "50mb"  // Increased for ML models
      }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "backend/main.py"
    }
  ],
  "functions": {
    "backend/main.py": {
      "memory": 3008,      // Max memory for AI operations
      "maxDuration": 60    // 60 seconds timeout
    }
  }
}
```

### Function Limits

**Hobby Plan (Free)**:
- Memory: Up to 1024 MB
- Duration: 10 seconds
- Deployments: Unlimited

**Pro Plan ($20/month)**:
- Memory: Up to 3008 MB
- Duration: 60 seconds
- Deployments: Unlimited
- Custom domains

## Environment-Specific Settings

### Development
```bash
vercel env add VERCEL_ENV development
```

### Preview (Staging)
```bash
vercel env add VERCEL_ENV preview
```

### Production
```bash
vercel env add VERCEL_ENV production
```

## Custom Domain

1. **Add Domain in Vercel Dashboard**
   - Go to Project Settings → Domains
   - Add your custom domain
   - Follow DNS configuration instructions

2. **Update CORS**
   The app automatically handles CORS for Vercel URLs

## Monitoring and Logs

### View Logs
```bash
vercel logs <deployment-url>
```

### Real-time Logs
```bash
vercel logs --follow
```

### Dashboard
- Analytics: https://vercel.com/dashboard/analytics
- Deployments: https://vercel.com/dashboard
- Function logs: Available per deployment

## Performance Optimization

### 1. **Cold Start Optimization**
```python
# In backend/main.py
# Pre-load models at startup
@app.on_event("startup")
async def startup_event():
    # Initialize services
    from backend.services.serpapi_service import serpapi_service
    logger.info("Services initialized")
```

### 2. **Caching**
```python
# Use Vercel KV for caching
from vercel_kv import kv

@app.get("/cached-data")
async def get_cached_data():
    cached = await kv.get("key")
    if cached:
        return cached
    # Fetch and cache
```

### 3. **Edge Functions**
For faster response times, consider Vercel Edge Functions for static content.

## CI/CD Pipeline

Vercel automatically deploys on:
- ✅ Push to `main` branch → Production
- ✅ Push to other branches → Preview deployments
- ✅ Pull requests → Preview deployments

### GitHub Integration
1. Install Vercel GitHub app
2. Connect repository
3. Automatic deployments on push

## Troubleshooting

### Issue: Build Fails
**Solution**: Check build logs in Vercel dashboard
```bash
vercel logs <deployment-url>
```

### Issue: Function Timeout
**Solution**: Optimize code or upgrade to Pro plan for 60s timeout

### Issue: Memory Limit Exceeded
**Solution**: 
- Reduce model size
- Use lazy loading
- Upgrade to Pro plan

### Issue: Environment Variables Not Working
**Solution**: 
```bash
vercel env pull  # Pull latest env vars
vercel --prod    # Redeploy
```

### Issue: Database Connection Fails
**Solution**: 
- Check DATABASE_URL format
- Ensure SSL mode is enabled
- Verify database allows connections from Vercel IPs

## Scaling

### Automatic Scaling
Vercel automatically scales based on traffic:
- 0 to millions of requests
- Global CDN distribution
- Automatic HTTPS

### Rate Limiting
Implement rate limiting for API endpoints:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/api/endpoint")
@limiter.limit("10/minute")
async def endpoint():
    return {"message": "Rate limited"}
```

## Cost Estimation

### Hobby Plan (Free)
- 100 GB bandwidth
- 100 hours serverless function execution
- Perfect for development and small projects

### Pro Plan ($20/month)
- 1 TB bandwidth
- 1000 hours serverless function execution
- Custom domains
- Team collaboration

### Enterprise
- Custom pricing
- Dedicated support
- SLA guarantees

## Security Best Practices

1. **Environment Variables**
   - Never commit secrets to Git
   - Use Vercel's encrypted environment variables
   - Rotate keys regularly

2. **CORS Configuration**
   ```python
   # Production CORS
   if os.getenv("VERCEL_ENV") == "production":
       allow_origins = ["https://yourdomain.com"]
   ```

3. **Rate Limiting**
   - Implement per-endpoint rate limits
   - Use Vercel's DDoS protection

4. **Authentication**
   - Use JWT tokens
   - Implement API key validation
   - Enable HTTPS only

## Webhooks Configuration

For WhatsApp webhooks, update Twilio:
```
Webhook URL: https://your-app.vercel.app/api/v1/whatsapp/webhook
```

## Testing Deployment

### Health Check
```bash
curl https://your-app.vercel.app/health
```

### API Test
```bash
curl -X POST https://your-app.vercel.app/api/v1/market-intelligence/scout-trends \
  -H "Content-Type: application/json" \
  -d '{"timeframe": "now 7-d"}'
```

## Rollback

If deployment fails:
```bash
vercel rollback
```

Or use the dashboard to promote a previous deployment.

## Advanced Features

### 1. **Preview Deployments**
Every branch gets a unique URL for testing

### 2. **Environment Branches**
```bash
vercel --prod           # Production
vercel --target preview # Preview
```

### 3. **Analytics**
Built-in Web Analytics and Web Vitals tracking

### 4. **Edge Config**
For ultra-fast global configuration:
```bash
vercel edge-config create
```

## Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Python on Vercel](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [Environment Variables](https://vercel.com/docs/concepts/projects/environment-variables)
- [Custom Domains](https://vercel.com/docs/concepts/projects/custom-domains)
- [Vercel CLI](https://vercel.com/docs/cli)

## Support

- Community: [Vercel Discussions](https://github.com/vercel/vercel/discussions)
- Discord: [Vercel Discord](https://vercel.com/discord)
- Email: support@vercel.com (Pro/Enterprise)

## Next Steps

1. ✅ Deploy to Vercel
2. ✅ Set up custom domain
3. ✅ Configure monitoring
4. ✅ Set up CI/CD
5. ✅ Implement caching
6. ✅ Add rate limiting
7. ✅ Monitor performance
8. ✅ Scale as needed
