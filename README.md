# hospital-management
medium level project
# Hospital Role-Based Authentication

A Django-based hospital management system with **role based access control**, built with **Django REST Framework**, **Celery**, **Redis**, and **MySQL**, all containerized using Docker.

---

## 🏥 Features

- User registration, login, logout, and token-based authentication (JWT or DRF tokens).  
- Role-based permissions (e.g. Admin, Doctor, Nurse, Patient) to control access to endpoints.  
- Asynchronous task handling with Celery + Redis (for sending emails, background jobs, etc.).  
- MySQL as primary relational database.  
- Dockerized architecture to simplify local development / deployment.

---

## 📁 Repository Structure

├── Dockerfile
├── docker-compose.yml
├── manage.py
├── requirements.txt
├── <your_app_folders>
├── role_based_auth/ ← Django project folder (settings, urls, wsgi, etc.)
├── account/ ← App for user / authentication & registration
└── ...


Adjust structure names based on your actual folder names.

---

## 🛠️ Prerequisites

- Docker  
- Docker Compose (v2+ preferably)  
- Basic familiarity with Django, REST Framework, Celery  

---

**Clone the repo**

   ```bash
   git clone https://github.com/AYUSHIPATEL123/hospital-rolebased-authentication.git
   cd hospital-rolebased-authentication

🧰 Dependencies

Your requirements.txt should include (at minimum):

Django>=4.0
djangorestframework
celery
redis
mysqlclient
django-redis
PyJWT (if using JWT)


Adjust version pins as needed.

🔐 Role-based Access (How it works)

Users have roles (e.g. Admin, Doctor, Nurse, Patient).

Each API/view has permission logic (custom DRF permissions) that checks the user’s role.

Only users with appropriate roles can access certain endpoints (e.g. only Doctor role can see patient history, etc.).

🧪 Testing & Development Tips

Use docker-compose exec web python manage.py shell to interact with Django models.

Tail celery tasks or test asynchronous tasks by creating simple example tasks and invoking them.

Use Django’s debug settings locally for easier error tracing.

Make sure containers are communicating: test inside web container:

docker-compose exec web ping redis


If you change dependencies, rebuild with docker-compose up -d --build.

🧾 Troubleshooting

Redis connection refused → Ensure CELERY_BROKER_URL and CELERY_RESULT_BACKEND point to redis service, not 127.0.0.1.

Database errors → Check MySQL credentials in docker-compose.yml & settings.

Service startup order → Use depends_on in Docker Compose.

Container names mismatch → Use docker ps to see actual names if using docker exec.
