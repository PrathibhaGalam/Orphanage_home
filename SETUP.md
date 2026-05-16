# Setup Instructions for Orphanage Management System

## Step 1: Environment Setup

### Prerequisites
- Python 3.8 or higher
- MySQL 5.7 or higher
- pip (Python package manager)

### Installation Steps

1. **Create Virtual Environment**
```bash
cd orphanagehome
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Setup Environment Variables**
```bash
# Copy the example file
cp .env.example .env

# Edit .env with your configuration
# - Change DB_PASSWORD to your MySQL password
# - Keep other settings as default for development
```

4. **Create MySQL Database**
```sql
CREATE DATABASE orphanage_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

5. **Initialize Database**
```bash
python
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context():
>>>     db.create_all()
>>> exit()
```

6. **Run the Application**
```bash
python run.py
```

Access the app at: http://localhost:5000

## Default Accounts (for testing)

After running the app, register new accounts through the registration page.

## Project Structure

```
orphanagehome/
├── app/                    # Flask application
│   ├── auth/              # Authentication routes
│   ├── admin/             # Admin panel routes
│   ├── donor/             # Donor portal routes
│   ├── api/               # REST API routes
│   ├── templates/         # HTML templates
│   └── static/            # CSS, JS files
├── database/              # Database models
├── run.py                 # Application entry point
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
└── .env                   # Environment variables
```

## Features Implemented in Step 1

✅ Flask project structure with blueprints
✅ Database models (User, Orphan, Orphanage, Staff, Donation, Report)
✅ Authentication system
✅ Admin routes template
✅ Donor portal template
✅ REST API endpoints
✅ Base templates with Bootstrap 5
✅ Static files (CSS, JS)

## Next Steps

- Step 2: Create complete MySQL schema
- Step 3: Implement full authentication
- Step 4: Build admin CRUD operations
- Step 5: Implement donor portal features
