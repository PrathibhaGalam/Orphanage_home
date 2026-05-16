# Quick Start - Run the Application

## 1. Open Terminal in Project Root
```
cd c:\Users\prath\OneDrive\Documents\PROJECTS\orphanagehome
```

## 2. Create Virtual Environment
```
python -m venv venv
venv\Scripts\activate
```

## 3. Install Dependencies
```
pip install -r requirements.txt
```

## 4. Create Environment File
```
copy .env.example .env
```
Edit `.env` and update your MySQL password

## 5. Create MySQL Database
Open MySQL CLI and run:
```sql
CREATE DATABASE orphanage_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## 6. Run Flask Application
```
python run.py
```

## 7. Access Application
- **URL:** http://localhost:5000
- **Default:** Landing page

## 8. Test Registration
1. Click "Register"
2. Create account with role: **Donor** or **Admin**
3. Login with your credentials

## File Structure Created
```
orphanagehome/
├── app/                              ✅ Flask app package
│   ├── __init__.py                  ✅ App factory
│   ├── auth/routes.py              ✅ Login/Register endpoints
│   ├── admin/routes.py             ✅ Admin CRUD endpoints
│   ├── donor/routes.py             ✅ Donor portal endpoints
│   ├── api/routes.py               ✅ REST API endpoints
│   ├── static/
│   │   ├── css/style.css           ✅ Bootstrap theme
│   │   └── js/main.js              ✅ JavaScript utilities
│   └── templates/
│       ├── base.html               ✅ Base template
│       ├── auth/login.html         ✅ Login form
│       ├── auth/register.html      ✅ Registration form
│       ├── auth/profile.html       ✅ User profile
│       ├── admin/dashboard.html    ✅ Admin stats
│       ├── admin/orphanages/       ✅ Orphanage CRUD forms
│       ├── admin/orphans/          ✅ Orphan CRUD forms
│       ├── admin/donations/list.html ✅ Donation list
│       └── donor/                  ✅ Donor portal templates
├── database/models.py               ✅ SQLAlchemy models
├── config.py                        ✅ Flask configuration
├── run.py                           ✅ Application entry point
├── requirements.txt                 ✅ Python dependencies
├── .env.example                     ✅ Environment template
└── SETUP.md                         ✅ Full setup guide
```

## What's Next?
- **Step 2:** Configure MySQL & test database
- **Step 3:** Test login/register system
- **Step 4:** Build complete admin CRUD
- **Step 5:** Implement payment integration
- **Step 6:** Add location/map features
