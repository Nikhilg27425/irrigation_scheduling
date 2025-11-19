"""
Database migration script to add preferred_language column
"""
import sqlite3
import os

def migrate_database():
    db_path = 'instance/farmers.db'
    
    if not os.path.exists(db_path):
        print("Database doesn't exist yet. Will be created on first run.")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if column exists
        cursor.execute("PRAGMA table_info(user)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'preferred_language' not in columns:
            print("Adding preferred_language column...")
            cursor.execute("ALTER TABLE user ADD COLUMN preferred_language VARCHAR(10) DEFAULT 'en'")
            conn.commit()
            print("✓ Migration successful!")
        else:
            print("Column already exists. No migration needed.")
        
        conn.close()
    except Exception as e:
        print(f"Migration error: {e}")
        print("Recommendation: Delete instance/farmers.db and restart the app")

if __name__ == '__main__':
    migrate_database()
