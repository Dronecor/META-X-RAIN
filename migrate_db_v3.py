from backend.database import engine
from sqlalchemy import text, inspect

def run_migrations():
    print("Running migrations...")
    inspector = inspect(engine)
    columns = [c['name'] for c in inspector.get_columns('products')]
    
    if 'visual_description' not in columns:
        with engine.connect() as conn:
            try:
                conn.execute(text("ALTER TABLE products ADD COLUMN visual_description TEXT"))
                conn.commit()
                print("Added visual_description column to products")
            except Exception as e:
                print(f"Error adding column: {e}")
    else:
        print("visual_description column already exists")

if __name__ == "__main__":
    run_migrations()
