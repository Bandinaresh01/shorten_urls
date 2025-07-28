from flask import Blueprint, request, redirect, render_template, jsonify
from models import insert_url, get_url_by_shortcode, increment_click, get_stats
from utils import generate_short_id, is_valid_url
from datetime import datetime
import sqlite3

shortener_bp = Blueprint('shortener', __name__)

@shortener_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@shortener_bp.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.form.get('long_url')
    expiry_str = request.form.get('expiry_date')

    if not is_valid_url(long_url):
        return jsonify({'error': 'Invalid URL'}), 400

    expiry_date = None
    if expiry_str:
        try:
            expiry_date = datetime.strptime(expiry_str, '%Y-%m-%d')
        except ValueError:
            return jsonify({'error': 'Invalid expiry format. Use YYYY-MM-DD'}), 400

    # Generate short code
    short_id = generate_short_id(long_url)
    
    # Check for collisions and regenerate if needed
    while get_url_by_shortcode('instance/shortener.db', short_id):
        short_id = generate_short_id(long_url + str(datetime.utcnow()))

    try:
        insert_url('instance/shortener.db', long_url, short_id, expiry_date.isoformat() if expiry_date else None)
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Short URL conflict'}), 500

    return jsonify({
        'short_url': request.host_url + short_id,
        'long_url': long_url,
        'expiry_date': expiry_date.strftime('%Y-%m-%d') if expiry_date else None
    })

@shortener_bp.route('/<short_id>')
def redirect_url(short_id):
    result = get_url_by_shortcode('instance/shortener.db', short_id)

    if result is None:
        return jsonify({'error': 'URL not found'}), 404

    original_url, clicks, expiry_date = result

    # Check if URL has expired
    if expiry_date:
        try:
            expiry_dt = datetime.fromisoformat(expiry_date)
            if expiry_dt < datetime.utcnow():
                return jsonify({'error': 'Short URL has expired'}), 410
        except ValueError:
            pass  # Invalid date format, ignore expiry check

    # Increment click count
    increment_click('instance/shortener.db', short_id)
    
    return redirect(original_url)

@shortener_bp.route('/stats/<short_id>', methods=['GET'])
def url_stats(short_id):
    result = get_stats('instance/shortener.db', short_id)
    if not result:
        return jsonify({'error': 'Short URL not found'}), 404

    original_url, clicks, created_at, expiry_date = result

    return jsonify({
        'original_url': original_url,
        'short_url': request.host_url + short_id,
        'clicks': clicks,
        'created_at': created_at,
        'expiry_date': expiry_date
    })
