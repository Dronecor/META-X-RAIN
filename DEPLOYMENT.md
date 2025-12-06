# Deployment Guide - Agentic AI CRM

## 🚀 Quick Start (Local Development)

### Prerequisites
- ✅ Python 3.10+ installed
- ✅ Git installed (optional)
- ✅ Windows PowerShell

### 1. Environment Setup

**Create/Verify `.env` file in project root:**
```env
# Project Config
PROJECT_NAME="Agentic AI CRM"
SECRET_KEY=your-secret-key-here

# Database (SQLite for local, PostgreSQL for production)
DATABASE_URL=sqlite:///./agentic_crm.db

# AI / Groq
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=llama-3.3-70b-versatile

# Messaging (Optional for WhatsApp)
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
TWILIO_WHATSAPP_NUMBER=whatsapp:+1234567890

# Email (Optional)
SENDGRID_API_KEY=your-sendgrid-key

# Backend URL
BACKEND_API_URL=http://localhost:8000/api/v1
```

### 2. Install Dependencies

```powershell
pip install -r backend/requirements.txt
```

### 3. Launch Application

**Option A: Automated Startup (Recommended)**
```powershell
PowerShell -ExecutionPolicy Bypass -File .\run_locally.ps1
```

This will automatically start:
- **Backend API** → `http://localhost:8000`
- **Admin Dashboard** → `http://localhost:8501`
- **Customer App** → `http://localhost:8502`

**Option B: Manual Startup**
```powershell
# Terminal 1: Backend
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Admin Dashboard
python -m streamlit run frontend_admin/app.py --server.port 8501

# Terminal 3: Customer App
python -m streamlit run frontend_customer/app.py --server.port 8502
```

---

## 🔐 Access & Credentials

### Admin Dashboard (`http://localhost:8501`)
- **Username**: `admin`
- **Password**: `admin`
- **Features**: View conversations, customer profiles, system health

### Customer App (`http://localhost:8502`)
- **Sign In**: Enter name and email
- **Features**: Chat with AI, view past conversations, get product recommendations

### API Documentation (`http://localhost:8000/docs`)
- Interactive Swagger UI for testing endpoints

---

## 🌐 Production Deployment

### Option 1: Cloud Platform (Render/Railway/Heroku)

**1. Update `.env` for Production:**
```env
DATABASE_URL=postgresql://user:password@host:5432/dbname
SECRET_KEY=<generate-strong-key>
```

**2. Deploy Backend:**
- Push code to GitHub
- Connect repository to Render/Railway
- Set environment variables in platform dashboard
- Deploy command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

**3. Deploy Frontends:**
- Admin: `streamlit run frontend_admin/app.py --server.port $PORT`
- Customer: `streamlit run frontend_customer/app.py --server.port $PORT`

### Option 2: Docker Deployment

**1. Build Images:**
```bash
docker-compose build
```

**2. Start Services:**
```bash
docker-compose up -d
```

**3. Access:**
- Backend: `http://localhost:8000`
- Admin: `http://localhost:8501`
- Customer: `http://localhost:8502`

---

## 📱 WhatsApp Integration (Optional)

### 1. Expose Local Backend (Development)
```bash
ngrok http 8000
```

### 2. Configure Twilio Webhook
- Go to Twilio Console → WhatsApp Sandbox
- Set webhook URL: `https://your-ngrok-url.ngrok.io/api/v1/whatsapp/webhook`
- Method: `POST`

### 3. Test
Send "Hello" to your Twilio WhatsApp number. The AI should respond!

---

## 🔧 Troubleshooting

### Backend Won't Start
```powershell
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill process if needed
taskkill /PID <process-id> /F
```

### Database Issues
```powershell
# Reset database (WARNING: Deletes all data)
Remove-Item agentic_crm.db
# Restart backend to recreate tables
```

### Streamlit Port Conflicts
```powershell
# Use different ports
streamlit run frontend_admin/app.py --server.port 8503
```

### Missing Dependencies
```powershell
pip install --upgrade -r backend/requirements.txt
```

---

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Customer App                       │
│              (Streamlit - Port 8502)                │
└──────────────────┬──────────────────────────────────┘
                   │
                   │ HTTP/REST
                   │
┌──────────────────▼──────────────────────────────────┐
│              Backend API (FastAPI)                   │
│                  Port 8000                          │
│  ┌─────────────────────────────────────────────┐   │
│  │  Agent Router                                │   │
│  │  ├─ Sales Agent (Groq LLaMA 3.3)           │   │
│  │  ├─ Support Agent                          │   │
│  │  └─ Visual Search Agent                    │   │
│  └─────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────┐   │
│  │  Chat History Service                       │   │
│  │  └─ Auto-summarization                     │   │
│  └─────────────────────────────────────────────┘   │
└──────────────────┬──────────────────────────────────┘
                   │
                   │
┌──────────────────▼──────────────────────────────────┐
│           SQLite Database                           │
│  ├─ Users                                          │
│  ├─ Conversations                                  │
│  ├─ Messages                                       │
│  └─ Orders, Products, etc.                        │
└─────────────────────────────────────────────────────┘
                   ▲
                   │
┌──────────────────┴──────────────────────────────────┐
│              Admin Dashboard                         │
│              (Streamlit - Port 8501)                │
└─────────────────────────────────────────────────────┘
```

---

## ✅ Verification Checklist

- [ ] Backend API responds at `/health`
- [ ] Admin can log in and view conversations
- [ ] Customer can sign in and chat
- [ ] Messages are saved to database
- [ ] Conversation summaries are generated
- [ ] Images display correctly in chat
- [ ] Multiple conversations can be created
- [ ] Past conversations load on login

---

## 🎯 Demo Script

**For Hackathon Presentation:**

1. **Start System**: Run `run_locally.ps1`
2. **Customer Flow**:
   - Open Customer App
   - Sign in as "Sarah Johnson"
   - Ask: "Show me a summer dress"
   - Start new conversation
   - Ask: "I need shoes for a wedding"
3. **Admin Flow**:
   - Open Admin Dashboard
   - Log in with admin/admin
   - View Sarah's conversations
   - Show conversation summaries
   - Demonstrate system health check

---

## 📝 Notes

- **Database**: SQLite for development, migrate to PostgreSQL for production
- **Security**: Change default admin password before production
- **API Keys**: Never commit `.env` to version control
- **Scaling**: Consider Redis for session management in production
- **Monitoring**: Add logging service (e.g., Sentry) for production

---

## 🆘 Support

For issues or questions:
1. Check logs in terminal windows
2. Verify `.env` configuration
3. Ensure all dependencies are installed
4. Check `README.md` for additional context
