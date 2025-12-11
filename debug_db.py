from sqlalchemy import create_engine, text
from backend.config import settings

def check_db():
    if not settings.DATABASE_URL:
        # Fallback similar to main app
        url = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
    else:
        url = settings.DATABASE_URL

    if "sqlite" in url:
        connect_args = {"check_same_thread": False}
    else:
        connect_args = {}

    print(f"Connecting to: {url}")
    try:
        engine = create_engine(url, connect_args=connect_args)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='products';"))
            if result.fetchone():
                print("Table 'products' exists.")
                # Check columns
                cols = conn.execute(text("PRAGMA table_info(products)")).fetchall()
                col_names = [c[1] for c in cols]
                print(f"Columns: {col_names}")
                if 'visual_description' in col_names:
                    print("SUCCESS: visual_description column exists.")
                else:
                    print("FAILURE: visual_description column MISSING.")
            else:
                print("Table 'products' does NOT exist.")
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    check_db()
