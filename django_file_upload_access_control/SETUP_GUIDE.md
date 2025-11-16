# Django File Upload Access Control API - Setup & Running Guide

## ✅ Project Successfully Upgraded & Running!

The Django File Upload & Access Control API is now set up and running with all the latest upgrades.

### 🚀 Server Status
- **Status**: ✅ Running
- **URL**: http://localhost:8000
- **API Endpoint**: http://localhost:8000/api/

### 📦 Key Upgrades Applied

#### Dependencies (requirements.txt)
- Django: 4.2 → 5.2.8 (latest LTS)
- djangorestframework: 3.16.1
- djangorestframework-simplejwt: 5.5.1
- cryptography: 46.0.3
- python-dotenv: 1.2.1
- gunicorn: 23.0.0 (production server)
- whitenoise: 6.11.0 (static files)
- django-cors-headers: 4.9.0 (CORS support)

#### Infrastructure (Dockerfile)
- Python: 3.11 → 3.12-slim
- Production-ready with gunicorn (3 workers)
- Optimized layering and caching

#### Configuration (settings.py)
✓ Security: HTTPS redirects, HSTS, XSS protection
✓ JWT: Token lifetime, refresh tokens
✓ CORS: Configurable origins
✓ Password validators: All 4 Django validators enabled
✓ Database: SQLite with proper configuration
✓ Static files: WhiteNoise compression

#### Code Quality (views.py)
✓ Better error handling with proper HTTP status codes
✓ Comprehensive docstrings
✓ Password strength validation (min 8 chars)
✓ Improved exception handling
✓ Transaction safety

#### Database Models (models.py)
✓ Added helper methods: is_owner(), is_allowed_user(), has_access()
✓ Database indexes for performance
✓ Proper Meta configuration

#### Admin Interface (admin.py)
✓ Custom admin class with list displays
✓ Search functionality
✓ Filtering by date, encryption status, owner
✓ User isolation (non-superusers see only their files)

---

## 🔐 Admin Access

**URL**: http://localhost:8000/admin/
**Username**: admin
**Password**: admin123

---

## 📡 API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
  - Body: `{"username": "user", "password": "pass"}`
  
- `POST /api/auth/token/` - Get JWT token
  - Body: `{"username": "user", "password": "pass"}`

### File Operations
- `POST /api/files/upload/` - Upload encrypted file
  - Headers: `Authorization: Bearer {token}`
  - Body: FormData with `file` and optional `share_with` list
  
- `GET /api/files/` - List your files
  - Headers: `Authorization: Bearer {token}`
  
- `GET /api/files/{id}/download/` - Download file
  - Headers: `Authorization: Bearer {token}`
  - Query param: `?token={signed_token}` for public access
  
- `GET /api/files/{id}/signed-url/` - Generate signed URL
  - Headers: `Authorization: Bearer {token}`
  - Query param: `?expires=300` (seconds, default 300)

---

## 📁 Project Structure

```
django_file_upload_access_control/
├── manage.py                  # Django management
├── requirements.txt           # Updated dependencies
├── Dockerfile                 # Production Docker image
├── .env                      # Environment variables (with Fernet key)
├── .env.example              # Example configuration
├── test_api.py               # API test script
│
├── file_share/               # Django project settings
│   ├── settings.py           # ✅ UPGRADED - Enhanced security & config
│   ├── urls.py               # Project URLs
│   ├── wsgi.py              # WSGI application
│
├── files/                    # Main Django app
│   ├── models.py             # ✅ UPGRADED - Better models with helpers
│   ├── views.py              # ✅ UPGRADED - Better error handling
│   ├── serializers.py        # API serializers
│   ├── urls.py               # App URLs
│   ├── admin.py              # ✅ UPGRADED - Custom admin interface
│   └── migrations/           # Database migrations
│
└── examples/
    └── generate_fernet_key.py # Key generation utility
```

---

## 🔑 Environment Variables (.env)

```
DEBUG=True
SECRET_KEY=django-insecure-dev-key-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1
FERNET_KEY=EzC5SMdH8EEsTMsvMzNmCEFZ_-lg1EzieJNYhlsDnBQ=
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

---

## 🛠️ Development Server

The server is currently running with the command:
```powershell
python manage.py runserver 0.0.0.0:8000
```

### Stop the Server
Press `CTRL+BREAK` in the terminal running the server.

### Restart the Server
```powershell
cd C:\Users\MUDABBIR\Downloads\django_file_upload_access_control\django_file_upload_access_control
python manage.py runserver
```

---

## 📊 Features Implemented

✅ **User Authentication**
- Registration with password validation
- JWT token-based authentication
- Token refresh mechanism

✅ **File Management**
- Encrypted file uploads (Fernet encryption)
- Owner-based access control
- Share files with specific users

✅ **Security**
- File encryption at rest
- Time-limited signed download URLs
- CORS configuration
- HTTPS ready (with production settings)
- HSTS headers
- XSS protection

✅ **Admin Interface**
- Manage files and users
- Search and filter capabilities
- Bulk operations

---

## 🧪 Testing the API

Use the provided `test_api.py` script:
```powershell
python test_api.py
```

Or test manually with curl/Postman:
```bash
# Register user
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'

# Get token
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'

# List files (replace TOKEN with actual token)
curl -X GET http://localhost:8000/api/files/ \
  -H "Authorization: Bearer TOKEN"
```

---

## 📝 Notes

- Database: SQLite (db.sqlite3) - suitable for development
- Media files: Stored in `uploaded_media/` directory
- All files are encrypted using Fernet before storage
- Migrations have been applied successfully

---

## 🚀 Next Steps

### For Production Deployment:
1. Set `DEBUG=False` in .env
2. Use a proper database (PostgreSQL recommended)
3. Use gunicorn instead of runserver
4. Add proper SECRET_KEY
5. Configure ALLOWED_HOSTS
6. Use HTTPS with proper SSL certificates
7. Set up proper environment variables on the server

---

**Project upgraded and running successfully! 🎉**
