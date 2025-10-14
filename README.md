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

Manual Setup (Without Docker)

Create and activate a Python virtual environment:

python3 -m venv venv
source venv/bin/activate


Install dependencies:

pip install -r requirements.txt


Ensure MySQL and Redis are running and accessible.

Environment Variables

Copy .env.example (or similar) to .env and fill in:

DJANGO_SECRET_KEY=your_secret_key
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

Database & Migrations

Inside the Django container (or your virtualenv):

python manage.py makemigrations
python manage.py migrate


Create a superuser:

python manage.py createsuperuser

Running the Application

(Docker) Already started via docker-compose up — API available on http://localhost:8000 (or configured port)

(Manual) Run Django server:

python manage.py runserver 0.0.0.0:8000


To run Celery worker:

celery -A your_project_name worker --loglevel=info


To run Celery beat (if scheduled tasks):

celery -A your_project_name beat --loglevel=info
