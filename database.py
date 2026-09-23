"""
Legacy database initialization entry point.
Delegates to database/db_manager.py for unified schema management.
"""
from database.db_manager import DatabaseManager

def init_db():
    db = DatabaseManager()
    return db

if __name__ == "__main__":
    db = init_db()
    print(f"CyberGuard database initialized successfully at: {db.db_path}")