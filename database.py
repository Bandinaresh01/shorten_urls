import os
from models import create_tables

# Define the path for the SQLite DB
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_NAME = "shortener.db"
DB_PATH = os.path.join(BASE_DIR, "instance", DB_NAME)

# Call table creation on startup
def init_db():
    # Ensure instance directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    if not os.path.exists(DB_PATH):
        print("[INFO] Creating new database...")
    create_tables(DB_PATH)

# Utility for reuse across app
def get_db_path():
    return DB_PATH
