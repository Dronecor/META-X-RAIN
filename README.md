# ShopBuddy - AI Fashion Assistant

A modern AI-powered fashion retail CRM with conversational shopping assistance, order management, and intelligent product recommendations.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Installation

1. **Clone and navigate to the project**
```bash
cd "META hackathon"
```

2. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys (Groq, etc.)
```

3. **Install dependencies**
```bash
# Backend
pip install -r backend/requirements.txt

# Frontend
npm install
```

4. **Run the application**
```bash
# Start backend (Terminal 1)
python -m uvicorn backend.main:app --reload

# Start frontend (Terminal 2)
npm run dev
```

5. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📁 Project Structure

```
├── app/                    # Next.js frontend
│   ├── components/         # React components
│   ├── page.jsx           # Main chat interface
│   └── layout.jsx         # App layout
├── backend/               # FastAPI backend
│   ├── agents/           # AI agents (sales, support, etc.)
│   ├── api/              # API endpoints
│   ├── services/         # Business logic
│   └── main.py           # FastAPI app
├── .env                  # Environment variables
└── README.md            # This file
```

## ✨ Features

### Customer Features
- 🛍️ **Conversational Shopping**: Natural chat interface for product discovery
- 📦 **Order Management**: View order details, track status, cancel orders
- 💬 **Smart Conversations**: Auto-generated contextual chat titles
- ⏰ **Conversation History**: Timestamped chats sorted by recency
- 🎨 **Product Recommendations**: AI-powered suggestions with images

### Technical Features
- 🤖 **AI Agents**: Specialized agents for sales, support, and market intelligence
- 🔍 **Vector Search**: Semantic product search using embeddings
- 📊 **Analytics**: Customer journey tracking and insights
- 🔐 **Secure**: Environment-based configuration
- 📱 **Responsive**: Mobile-friendly design

## 🛠️ Configuration

### Required Environment Variables

```env
# AI/LLM
GROQ_API_KEY=your_groq_api_key

# Optional
SERPAPI_API_KEY=your_serpapi_key  # For web scouting
BACKEND_API_URL=http://localhost:8000/api/v1
```

See `.env.example` for all available options.

## 📚 Documentation

- **ARCHITECTURE.md** - System architecture and design
- **CRM_RULES.md** - Business rules and AI agent behavior
- **SETUP_GUIDE.md** - Detailed setup instructions
- **DEPLOYMENT_CHECKLIST.md** - Production deployment guide
- **VERCEL_DEPLOYMENT.md** - Vercel-specific deployment
- **SERPAPI_GUIDE.md** - Web scouting integration
- **QUICK_REFERENCE.md** - API and command reference

## 🎯 Key Technologies

- **Frontend**: Next.js 14, React, CSS Modules
- **Backend**: FastAPI, Python 3.8+
- **AI**: Groq (Llama models), LangChain
- **Database**: SQLite (development), PostgreSQL (production)
- **Deployment**: Vercel (frontend), Railway/Render (backend)

## 🔧 Development

### Backend Development
```bash
# Run with auto-reload
python -m uvicorn backend.main:app --reload

# Run tests
pytest

# Check API docs
open http://localhost:8000/docs
```

### Frontend Development
```bash
# Run dev server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

## 📦 Order Management

Customers can:
- View all their orders with status badges
- See order details (items, dates, status)
- Cancel pending orders
- Track shipment status

## 💬 Conversation Features

- **Auto-Generated Titles**: Chat titles based on conversation context
- **Timestamps**: Relative time display (e.g., "5m ago", "2h ago")
- **Sorted History**: Newest conversations first
- **Context Preservation**: Each chat maintains its own history

## 🚢 Deployment

### Vercel (Frontend)
```bash
vercel deploy
```

### Backend (Railway/Render)
1. Connect your Git repository
2. Set environment variables
3. Deploy automatically on push

See `DEPLOYMENT_CHECKLIST.md` for detailed deployment steps.

## 🤝 Contributing

This is a hackathon project. For production use, consider:
- Adding authentication (OAuth, JWT)
- Implementing rate limiting
- Adding comprehensive error handling
- Setting up monitoring and logging
- Adding automated tests

## 📄 License

MIT License - See LICENSE file for details

## 🆘 Support

For issues or questions:
1. Check the documentation in the `/docs` folder
2. Review `QUICK_REFERENCE.md` for common commands
3. Check the API documentation at `/docs` endpoint

---

**Built with ❤️ for META Hackathon**
