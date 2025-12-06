from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Agentic AI CRM"
    API_V1_STR: str = "/api/v1"
    
    # Database
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_SERVER: str | None = None
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str | None = None
    DATABASE_URL: str | None = None

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # AI / Groq
    GROQ_API_KEY: str
    GROQ_MODEL: str = "llama3-70b-8192"

    # Services
    TWILIO_ACCOUNT_SID: str | None = None
    TWILIO_AUTH_TOKEN: str | None = None
    TWILIO_WHATSAPP_NUMBER: str | None = None
    
    SENDGRID_API_KEY: str | None = None
    
    PINECONE_API_KEY: str | None = None
    PINECONE_ENV: str | None = None

    class Config:
        import os
        env_file = os.path.join(os.path.dirname(__file__), ".env")
        extra = "ignore" # Allow extra fields in .env

settings = Settings()
