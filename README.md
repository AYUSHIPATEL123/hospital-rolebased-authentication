# Hospital Role-Based Authentication

A Django + DRF project implementing **role-based access control** (RBAC) for a hospital management system. Users are assigned roles (Admin, Doctor, Nurse, Patient), and each role has permissions to perform certain operations via REST APIs.

---

## Table of Contents

- [Features](#features)  
- [Tech Stack & Architecture](#tech-stack--architecture)  
- [Setup & Installation](#setup--installation)  
  - [Prerequisites](#prerequisites)  
  - [Clone & Docker Setup](#clone--docker-setup)  
  - [Manual Setup (Without Docker)](#manual-setup-without-docker)  
  - [Environment Variables](#environment-variables)  
  - [Database & Migrations](#database--migrations)  
- [Running the Application](#running-the-application)  
- [API Endpoints](#api-endpoints)  
- [Roles & Permissions](#roles--permissions)  
- [Usage Examples](#usage-examples)  
- [Testing & Development Tips](#testing--development-tips)  
- [Troubleshooting](#troubleshooting)  
- [Contributing](#contributing)  
- [License](#license)  
- [Acknowledgements](#acknowledgements)  

---

## Features

- User registration, login, logout  
- JWT (or DRF token) authentication  
- Role assignment and enforcement of access rules  
- CRUD operations on hospital entities (patients, doctors, etc.)  
- Background tasks support via Celery + Redis (for tasks such as sending emails, notifications)  
- MySQL (or other RDBMS) as database  
- Docker / Docker Compose setup for easy local development  

---

## Tech Stack & Architecture

| Layer | Technology |
|---|---|
| Backend / API | Python, Django, Django REST Framework |
| Authentication / Authorization | JWT (or DRF token), custom DRF permissions / decorators |
| Asynchronous Tasks | Celery + Redis |
| Database | MySQL |
| Caching / Broker | Redis |
| Containerization / Deployment | Docker, Docker Compose |

---

## Setup & Installation

### Prerequisites

- Docker & Docker Compose  
- Python 3.8+   
- MySQL server  
- Redis server  

### Clone & Docker Setup

```bash
git clone https://github.com/AYUSHIPATEL123/hospital-rolebased-authentication.git
cd hospital-rolebased-authentication
docker-compose up -d --build
```
Manual Setup (Without Docker)

1. Create and activate a Python virtual environment:
```bash
python3 -m venv venv
 venv/bin/activate.bat  (for windows)
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Ensure MySQL and Redis are running and accessible.

3. Environment Variables

Copy .env.example (or similar) to .env and fill in:

DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_HOST=localhost
DB_PORT=3306
DB_NAME=hospital_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password

REDIS_HOST=localhost
REDIS_PORT=6379

CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1

JWT_SECRET_KEY=your_jwt_secret   # if using JWT


Adjust host names (for Docker, often service names like mysql, redis) in your docker-compose.yml and Django settings.

4. Database & Migrations

Inside the Django container (or your virtualenv):

```bash
python manage.py makemigrations
python manage.py migrate
```

Create a superuser:
```bash
python manage.py createsuperuser
```
Running the Application

(Docker) Already started via docker-compose up — API available on http://localhost:8000 (or configured port)

(Manual) Run Django server:
```bash
python manage.py runserver 0.0.0.0:8000
```

To run Celery worker:
```bash
celery -A your_project_name worker --loglevel=info
```

To run Celery beat (if scheduled tasks):
```bash
celery -A your_project_name beat --loglevel=info
```
API Endpoints

Note: Below are sample endpoint paths. Replace with actual paths from your urls.py.

Endpoint	Method	Description	Access Role(s)
| Endpoint                  | Method                 | Description                       | Access Role(s)                               |
| ------------------------- | ---------------------- | --------------------------------- | -------------------------------------------- |
| `/api/auth/register/`     | `POST`                 | Register a new user               | Public                                       |
| `/api/auth/login/`        | `POST`                 | Obtain JWT / token                | Public                                       |
| `/api/auth/logout/`       | `POST`                 | Invalidate token / logout         | Authenticated                                |
| `/api/users/`             | `GET`, `POST`          | List or create users              | Admin                                        |
| `/api/users/<id>/`        | `GET`, `PUT`, `DELETE` | Retrieve, update or delete a user | Admin / Self (for profile)                   |
| `/api/patients/`          | `GET`, `POST`          | List or add patients              | Admin, Doctor, Nurse                         |
| `/api/patients/<id>/`     | `GET`, `PUT`           | View or update patient record     | Admin, Doctor, Nurse, (Patient viewing self) |
| `/api/doctors/`           | `GET`                  | List doctors                      | Admin, Authenticated                         |
| `/api/appointments/`      | `GET`, `POST`          | List or book appointments         | Authenticated (Patients), Admin, Doctor      |
| `/api/appointments/<id>/` | `GET`, `PUT`, `DELETE` | Manage specific appointment       | Based on role and ownership                  |


You may also have other entities (e.g. wards, treatments) with similar role-based access.

Roles & Permissions
Roles

Admin — full access to manage users, assign roles, view/modify all data

Doctor — view and modify patient medical data, manage appointments

Nurse — view patient details, record vitals / observations

Patient — view their own data, make appointments

Permission Enforcement

Custom DRF permission classes check a user’s role before granting access to views

Decorators or mixins (e.g. @role_required([“Doctor”, “Admin”])) can be used

Some endpoints may allow conditional access (e.g. patient can only GET their own records)

Usage Examples
Register a New Patient


```bash
POST /api/auth/register/
Content-Type: application/json
{
  "username": "john_doe",
  "password": "securepassword",
  "role": "Patient",
  "first_name": "John",
  "last_name": "Doe"
}
```

Login

```bash
POST /api/auth/login/
{
  "username": "john_doe",
  "password": "securepassword"
}
```
Response:
```bash
{
  "token": "jwt_token_here",
  "user": {
    "id": 5,
    "username": "john_doe",
    "role": "Patient"
  }
}
```

Fetch Patient Data (as Doctor)
```bash
GET /api/patients/12/
Authorization: Bearer <jwt_token>
```

If the user is a Doctor (or Admin), they can see data. If a Patient, only if it matches their own id.

Testing & Development Tips

Use Django shell to quickly test role logic:
```bash
python manage.py shell
from django.contrib.auth import get_user_model
U = get_user_model()
u = U.objects.get(pk=1); print(u.role)
```


Use docker-compose logs -f <service> to see live logs (web, celery, etc.)

Add unit tests for each permission / view

Rebuild images when dependencies change:
```bash
docker-compose up -d --build
```

Troubleshooting
| Problem                                 | Possible Cause                        | Solution                                                                            |
| --------------------------------------- | ------------------------------------- | ----------------------------------------------------------------------------------- |
| Cannot connect to Redis / Celery errors | Wrong broker URL, host name mismatch  | Confirm `CELERY_BROKER_URL`, `REDIS_HOST` in `.env`, use container names in Docker  |
| DB migrations failing                   | Incorrect DB credentials / host       | Verify `.env` and MySQL service in Docker                                           |
| Token authentication error              | JWT secret mismatch or missing header | Ensure correct `JWT_SECRET_KEY`, pass `Authorization` header properly               |
| Permission Denied                       | Role logic / permission class bug     | Check `has_permission` or `has_object_permission` in your custom permission classes |


Contributions are welcome! To contribute:

Fork this repo

Create a feature branch: git checkout -b feature/your-feature

Make changes, add tests

Commit and push your branch

Submit a pull request, explaining the changes

Please ensure your code follows PEP8 style and includes necessary tests/documentation.

License

This project is licensed under the MIT License — see LICENSE file.

Acknowledgements

Django, Django REST Framework

Celery, Redis

Docker, Docker Compose

Tutorials and blog posts on RBAC in Django / DRF
