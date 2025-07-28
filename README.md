# URL Shortener with Analytics

A Flask-based URL shortening service with built-in analytics and expiry functionality.

## Features

- 🔗 **URL Shortening**: Convert long URLs into short, manageable links
- 📊 **Analytics**: Track click counts and view detailed statistics
- ⏰ **Expiry Dates**: Set optional expiration dates for shortened URLs
- 🎯 **Collision Detection**: Automatic handling of duplicate short codes
- 📝 **Request Logging**: Comprehensive logging of all requests
- 💾 **SQLite Database**: Lightweight, file-based storage

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Bandinaresh01/shorten_urls.git
   cd shorten_urls
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. **Install dependencies**:
   ```bash
   pip install flask flask-sqlalchemy validators
   ```

## Usage

1. **Start the application**:
   ```bash
   python app.py
   ```

2. **Access the web interface**:
   Open your browser and go to `http://localhost:5000`

3. **Shorten a URL**:
   - Enter a long URL in the input field
   - Optionally set an expiry date
   - Click "Shorten URL" to generate a short link

4. **View statistics**:
   - Access `/stats/<short_code>` to view analytics for a specific URL

## API Endpoints

- `GET /` - Main interface
- `POST /shorten` - Create a new shortened URL
- `GET /<short_code>` - Redirect to original URL
- `GET /stats/<short_code>` - View URL statistics

## Project Structure

```
shorten_urls/
├── app.py                 # Main Flask application
├── database.py            # Database initialization
├── models.py              # SQLite database functions
├── utils.py               # Utility functions
├── routes/
│   └── shortener.py      # URL shortening routes
├── middleware/
│   └── logger.py         # Request logging
├── templates/
│   └── index.html        # Web interface
├── instance/
│   └── shortener.db      # SQLite database
└── logs/
    └── access.log        # Request logs
```

## Database Schema

The application uses SQLite with the following table structure:

```sql
CREATE TABLE urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_url TEXT NOT NULL,
    short_code TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL,
    clicks INTEGER DEFAULT 0,
    expiry_date TEXT
);
```

## Features in Detail

### URL Shortening
- Generates 6-character MD5-based short codes
- Handles collisions by regenerating codes
- Supports optional expiry dates

### Analytics
- Tracks click counts for each shortened URL
- Provides creation date and expiry information
- RESTful API for accessing statistics

### Security & Validation
- URL validation using the `validators` library
- SQL injection protection through parameterized queries
- Proper error handling and status codes

## Development

The application is built with:
- **Flask**: Web framework
- **SQLite**: Database
- **Bootstrap**: Frontend styling
- **JavaScript**: Dynamic form handling

## License

This project is open source and available under the MIT License. 