# Agentic AI CRM Architecture

## System Overview
The Agentic AI CRM is a specialized customer relationship management platform for fashion retail, powered by Meta Llama 3 (via Groq), FastAPI, and PostgreSQL. It features a multi-agent AI system to handle sales, support, and marketing.

## Core Components

### 1. Backend API (FastAPI)
- **Role**: Central brain of the application.
- **Tech**: FastAPI, Pydantic, SQLAlchemy.
- **Microservices/Modules**:
    - `api/`: REST endpoints for frontend and webhooks.
    - `agents/`: AI Agent logic (Sales, Support, Visual Search).
    - `rag/`: Vector search and product catalog management.
    - `services/`: External integrations (Twilio, SendGrid).

### 2. Database Layer
- **Relational DB**: PostgreSQL
    - Stores: Users, Orders, Products, Conversations, Complaints.
- **Vector DB**: Pinecone (or FAISS)
    - Stores: Product embeddings (CLIP/Text), Image embeddings.

### 3. AI Engine (Groq + Llama 3)
- **Model**: Meta Llama 3 (70B) via Groq Cloud API.
- **Orchestration**: LangChain.
- **Agents**:
    - **Sales Agent**: Recommendations, Upselling.
    - **Support Agent**: Refunds, Tracking, FAQs.
    - **Visual Search Agent**: Image similarity (CLIP).
    - **Market Intelligence**: Web Search (SerpAPI/Tavily) for price comparison.

### 4. Admin Dashboard (Streamlit)
- **Role**: Interface for business owners/admins.
- **Features**:
    - Manage Products & Inventory.
    - View Orders & Customers.
    - Monitor AI Conversations.
    - Handle Escalated Complaints.
    - Send Broadcasts (WhatsApp/Email).

### 5. Channels
- **WhatsApp (Twilio)**: Primary customer interface.
- **Email (SendGrid)**: Notifications (Order confirmation, Marketing).

## Data Flow

1. **Customer Message (WhatsApp)** -> **Twilio Webhook** -> **FastAPI Endpoint**.
2. **FastAPI** -> **Orchestrator**: Determines which agent should handle the intent.
    - *Intent: "Where is my order?"* -> **Support Agent**.
    - *Intent: "I want a red dress"* -> **Sales Agent**.
    - *Intent: Image Upload* -> **Visual Search Agent**.
3. **Agent Action**:
    - **RAG Lookup**: Search Vector DB for products/docs.
    - **DB Lookup**: Check Order status in Postgres.
    - **Web Search**: Check competitor prices.
4. **Response Generation**: Agent generates response via Groq Llama 3.
5. **Reply**: FastAPI -> Twilio -> WhatsApp User.

## Infrastructure
- **Containerization**: Docker.
- **Deployment**: Render / Railway / AWS.
- **CI/CD**: GitHub Actions (planned).

## Security
- **Authentication**: JWT for Admin Dashboard.
- **Secrets**: Environment variables (.env).
- **Access Control**: Role-based (Admin vs Support vs Customer).
