import hashlib
import sqlite3
import validators
from database import get_db_path

def generate_short_id(long_url):
    """
    Generate a short hash for the given URL.
    """
    return hashlib.md5(long_url.encode()).hexdigest()[:6]

def is_valid_url(url):
    """
    Validate the structure of a URL.
    """
    return validators.url(url)

def store_url_mapping(long_url, short_id):
    """
    Save a long URL and its short version to the DB.
    """
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute("INSERT INTO urls (long_url, short_url) VALUES (?, ?)", (long_url, short_id))
    conn.commit()
    conn.close()

def get_long_url(short_id):
    """
    Retrieve the original long URL for a given short ID.
    """
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute("SELECT long_url FROM urls WHERE short_url = ?", (short_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def is_short_id_taken(short_id):
    """
    Check if the generated short_id already exists.
    """
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM urls WHERE short_url = ?", (short_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists
