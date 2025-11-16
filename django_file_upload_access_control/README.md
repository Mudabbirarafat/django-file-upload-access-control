
# Django File Upload & Access Control API

This is a minimal Django + Django REST Framework project that demonstrates:
- User registration and JWT authentication (SimpleJWT)
- Encrypted file uploads using Fernet (cryptography)
- Owner-based access control + allowed-users sharing
- Time-limited signed download URLs (Django signing)

## Quick start (local)

1. Create and activate a Python venv:
   ```bash
   python -m venv venv
   source venv/bin/activate   # on Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

2. Set environment variables (create a `.env` file) - example provided:
   ```env
   SECRET_KEY=django-insecure-change-me
   FERNET_KEY=GENERATE_WITH_PYTHON_EXAMPLES (see below)
   DEBUG=1
   ```

   To generate a Fernet key in Python:
   ```python
   from cryptography.fernet import Fernet
   print(Fernet.generate_key().decode())
   ```

3. Run migrations and start server:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser   # optional
   python manage.py runserver
   ```

4. API endpoints
   - `POST /api/auth/register/` - register with `username` + `password`
   - `POST /api/auth/token/` - obtain JWT (username & password)
   - `POST /api/files/upload/` - upload file (authenticated). Form field `file`, optional `share_with` list of usernames (JSON array string).
   - `GET /api/files/` - list files you own or shared with you
   - `GET /api/files/<id>/download/` - download if owner or allowed user (or provide `?token=SIGNEDTOKEN` if using signed URL)
   - `GET /api/files/<id>/signed-url/?expires=300` - get signed, time-limited URL for download (owner only)

## Notes
- Uploaded files are encrypted on disk with Fernet using `FERNET_KEY`.
- Signed URLs are time-limited and validate signature before serving file.
- This scaffold uses SQLite for simplicity and local FileSystem storage.
