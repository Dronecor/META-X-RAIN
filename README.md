# Agentic AI CRM for Fashion Retail

A comprehensive, AI-powered CRM system built with FastAPI, Groq (Llama 3), and Streamlit.

## Features
- **Multi-Agent AI**: Specialized agents for Sales, Support, Visual Search, and Market Intelligence.
- **WhatsApp Integration**: Full customer journey via WhatsApp (Twilio).
- **Visual Search**: Upload images to find similar products.
- **RAG & Vector Search**: Intelligent product discovery using vector embeddings.
- **Admin Dashboard**: Streamlit-based control panel for business owners.
- **Automated Messaging**: Email notifications via SendGrid.

## Quick Start

### 1. Setup Environment
Copy the example environment file and fill in your API keys:
```bash
cp backend/.env.example backend/.env
```
Key requirements:
- `GROQ_API_KEY`: For Llama 3 models.
- `TWILIO_*`: For WhatsApp messaging.
- `SENDGRID_API_KEY`: For emails.

### 2. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 3. Run Backend
```bash
python -m uvicorn backend.main:app --reload
```
The API will be available at `http://localhost:8000`.

### 4. Run Admin Dashboard
Open a new terminal:
```bash
streamlit run frontend_admin/app.py
```

### 5. Expose for WhatsApp (Dev Mode)
Use ngrok to expose your local server:
```bash
ngrok http 8000
```
Update your Twilio Sandbox URL to: `https://<your-ngrok-url>/api/v1/whatsapp/webhook`

## Project Structure
- `backend/`: FastAPI application and AI agents.
  - `agents/`: Logic for specific AI personas.
  - `api/`: API route definitions.
  - `services/`: Integrations (Twilio, SendGrid, RAG).
  - `models.py`: Database schema.
- `frontend_admin/`: Streamlit dashboard code.

## Architecture
See [ARCHITECTURE.md](ARCHITECTURE.md) for a detailed system overview.
