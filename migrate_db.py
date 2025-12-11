from sqlalchemy import create_engine, text
from backend.config import settings

def migrate_db():
    engine = create_engine(settings.DATABASE_URL)
    with engine.connect() as conn:
        # Check if users table exists and bot_opt_in column needs adding
        try:
            conn.execute(text("ALTER TABLE users ADD COLUMN bot_opt_in BOOLEAN DEFAULT 0"))
            print("Added bot_opt_in column to users table.")
        except Exception as e:
            print(f"Column bot_opt_in might already exist or other error: {e}")

if __name__ == "__main__":
    migrate_db()
