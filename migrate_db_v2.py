from backend.database import engine, Base
from backend.models import Product
from sqlalchemy import text

def run_migrations():
    print("Running migrations...")
    # Add visual_description column if it doesn't exist
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE products ADD COLUMN visual_description TEXT"))
            print("Added visual_description column to products")
        except Exception as e:
            print(f"Migration note: visual_description might already exist or error: {e}")
            
    print("Migrations complete.")

if __name__ == "__main__":
    run_migrations()
