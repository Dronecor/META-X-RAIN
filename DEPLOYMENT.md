# Deployment Checklist

## 1. Prerequisites
- [ ] **Docker Installed**: Ensure Docker and Docker Compose are available.
- [ ] **Cloud Account**: Create accounts on Render, Railway, or AWS.
- [ ] **API Keys Obtained**:
  - Groq API Key
  - Twilio Account SID, Auth Token
  - SendGrid API Key
  - Pinecone API Key (optional for now)

## 2. Environment Configuration
- [ ] Create a `.env` file in the `backend/` directory based on `.env.example`.
- [ ] **Production Security**:
  - Generate a strong `SECRET_KEY` (e.g., `openssl rand -hex 32`).
  - Set `DEBUG=False` (if applicable in framework settings).

## 3. Database Migration
- [ ] Run the application once locally or use a migration script (Alembic recommended for production updates, though `Base.metadata.create_all` works for initial setup).

## 4. Docker Deployment
- [ ] **Build Image**:
  ```bash
  docker build -t agentic-crm-backend ./backend
  ```
- [ ] **Run Container**:
  ```bash
  docker run -p 8000:8000 --env-file backend/.env agentic-crm-backend
  ```

## 5. Exposing Webhook (Development)
- [ ] **Ngrok**:
  ```bash
  ngrok http 8000
  ```
- [ ] **Twilio Config**: Update WhatsApp Sandbox Configuration with the Ngrok URL + `/api/v1/whatsapp/webhook`.

## 6. Streamlit Dashboard
- [ ] Run separately or containerize:
  ```bash
  streamlit run frontend_admin/app.py
  ```

## 7. Verification
- [ ] Send "Hello" to the Twilio WhatsApp number.
- [ ] Check if the Agent replies.
- [ ] Check the Streamlit Dashboard for the conversation log.
