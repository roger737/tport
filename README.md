# Audit Tool

A self-hosted security audit management system implemented with Python and Flask.
The application runs fully offline and provides role based access control, audit
tracking and simple reporting.

## Features
- Flask backend with Blueprints
- Role based access control via custom decorators
- Audit lifecycle management with comments, findings and attachments
- SQLite database by default (PostgreSQL via `DATABASE_URL`)
- Session based authentication using Flask-Login
- CSV/PDF export of audits
- Docker and docker-compose for local deployment

## Usage
```
python seed.py   # initialise database with admin user (admin/admin)
python manage.py # run the development server
```

Then navigate to `http://localhost:5000` and log in with the seeded credentials.

This project is intentionally JavaScript free so it can operate in restricted
environments.
