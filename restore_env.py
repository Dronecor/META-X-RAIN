import secrets

secret_key = secrets.token_urlsafe(32)

env_content = f"""BACKEND_API_URL=http://localhost:8000/api/v1
SECRET_KEY={secret_key}
GROQ_API_KEY=ChangeMe_Add_Your_Groq_Key_Here
DATABASE_URL=sqlite:///./agentic_crm.db
"""

with open(".env", "w", encoding="utf-8") as f:
    f.write(env_content)

print(f"Restored .env with new SECRET_KEY. Please update GROQ_API_KEY.")
