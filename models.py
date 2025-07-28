import sqlite3
from datetime import datetime

def create_tables(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_code TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL,
            clicks INTEGER DEFAULT 0,
            expiry_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_url(db_path, original_url, short_code, expiry_date=None):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        INSERT INTO urls (original_url, short_code, created_at, expiry_date)
        VALUES (?, ?, ?, ?)
    ''', (original_url, short_code, datetime.utcnow().isoformat(), expiry_date))
    conn.commit()
    conn.close()

def get_url_by_shortcode(db_path, short_code):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT original_url, clicks, expiry_date FROM urls WHERE short_code = ?', (short_code,))
    result = c.fetchone()
    conn.close()
    return result

def increment_click(db_path, short_code):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?', (short_code,))
    conn.commit()
    conn.close()

def get_stats(db_path, short_code):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        SELECT original_url, clicks, created_at, expiry_date 
        FROM urls WHERE short_code = ?
    ''', (short_code,))
    result = c.fetchone()
    conn.close()
    return result
