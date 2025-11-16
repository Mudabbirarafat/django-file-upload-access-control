📁 Django File Upload & Access Control API

A secure, production-ready backend built with Django and Django REST Framework that provides encrypted file uploads, fine-grained access control, JWT-based authentication, and time-limited signed download URLs.
Designed for real-world systems where confidentiality, controlled access, and secure file sharing are essential.

🚀 Features
🔐 Authentication

JWT-based login & access tokens (SimpleJWT)

Username/password registration

Secure session handling

📤 Encrypted File Uploads

Files encrypted using Fernet (AES-256 level) before storage

Stored safely in MEDIA_ROOT/files/

👤 Access Control

Each file belongs to an owner

Owner can share file access with specific users

Only owner or allowed users can download

⏳ Signed Public Download Links

Generate time-limited download URLs

Uses Django’s TimestampSigner for tamper-proof tokens

Perfect for temporary external sharing

🧱 Backend Architecture

Django REST Framework

Encrypted storage layer

Token-based permission system

SQLite (default) but compatible with MySQL/PostgreSQL

DRY, clean, extendable code

🗂️ Tech Stack
Component	Technology
Backend Framework	Django 4+
API Framework	Django REST Framework
Auth System	JWT (SimpleJWT)
Encryption	cryptography.Fernet
Database	SQLite / MySQL / PostgreSQL
Deployment	Docker-ready
Environment	Python 3.10+

📦 Project Structure
django_file_upload_access_control/
│── file_share/              # Project settings & URLs
│── files/                   # File app (models, views, serializers)
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── serializers.py
│── uploaded_media/          # Encrypted uploaded files
│── Dockerfile
│── manage.py
│── requirements.txt
│── README.md
│── .env.example

⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/Mudabbirarafat/django-file-upload-access-control.git
cd django-file-upload-access-control

2️⃣ Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux/Mac

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Set up environment variables

Create a .env file:

SECRET_KEY=django-insecure-generate-new-key
DEBUG=1
FERNET_KEY=GENERATED_FERNET_KEY


Generate a secure Fernet key:

python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

5️⃣ Apply migrations
python manage.py migrate

6️⃣ Run the development server
python manage.py runserver

🔑 API Documentation

Below are all available REST API endpoints.

🧾 Authentication
Register
POST /api/auth/register/


Body:

{
  "username": "testuser",
  "password": "password123"
}

Login (JWT token)
POST /api/auth/token/


Body:

{
  "username": "testuser",
  "password": "password123"
}


Response:

{
  "access": "jwt_access_token",
  "refresh": "jwt_refresh_token"
}

📤 Upload File (Encrypted)
POST /api/files/upload/


Headers:

Authorization: Bearer <ACCESS_TOKEN>


Form-Data:

file: (binary file)

share_with: JSON list of usernames (optional)

Example:

share_with: ["friend1", "user2"]

📄 List Files (Owned + Shared)
GET /api/files/


Returns all files you own or shared with you.

📥 Download File
GET /api/files/<id>/download/


Accessible only to:

File owner
http://127.0.0.1:8000/admin/
Users added in allowed_users

OR via valid signed token

🔗 Generate Signed Download URL (Owner Only)
GET /api/files/<id>/signed-url/?expires=300


Response:

{
  "url": "/api/files/<id>/download/?token=<signed_token>",
  "expires_in": 300
}

🛡️ Security Highlights

AES-256 level encryption (Fernet)

JWT authentication + token expiry

Time-limited signed URL validation

Owner-based access control

Safe storage in isolated directory

🐳 Docker Support

Build the image:

docker build -t django-file-api .


Run container:

docker run -p 8000:8000 django-file-api

🧪 Testing

Example test:

python test_api.py

📌 Use Cases

✔ Secure document exchange
✔ Role-based file access systems
✔ Encrypted cloud storage backend
✔ University/enterprise file submission portals
✔ Temporary public download links

🤝 Contributing

Contributions are welcome!
Open a PR or raise an issue.

📜 License

MIT License — free for personal and commercial use.

⭐ Support the Project

If you find it helpful, please ⭐ the repo on GitHub!
