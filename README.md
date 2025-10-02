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
```
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









# Hospital Role-Based Authentication

## Overview

This project implements a robust role-based authentication system specifically designed for hospital environments. It allows for the secure management of user access based on their roles (e.g., Doctor, Nurse, Admin, Patient), ensuring that each user only has access to the functionalities and data relevant to their position. The system aims to enhance security, streamline operations, and maintain data privacy within a hospital setting.

## Features

*   **Role-Based Access Control (RBAC):** Define and assign distinct roles with specific permissions.
*   **Secure Authentication:** Implement secure user login and session management.
*   **User Management:** Admin panel to create, update, and delete user accounts and assign roles.
*   **Role Management:** Ability to define new roles and modify existing role permissions.
*   **Patient Data Protection:** Restrict access to sensitive patient information based on user roles.
*   **Scalable Architecture:** Designed to be easily integrated and scaled within existing or new hospital systems.
*   **Intuitive User Interface:** (If applicable, describe UI for admin/login)

## Technologies Used

*   **Backend:** [Python/Django,Celery,Redis,Docker]
*   **Frontend:** [HTML/CSS/JavaScript,Bootstrap]
*   **Database:** [MySQL]
*   **Authentication Library/Method:** [JWT]

## Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites

Before you begin, ensure you have the following installed:

*   [Python](https://www.python.org/) (if using Python)
*   [Git](https://git-scm.com/)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/AYUSHIPATEL123/hospital-rolebased-authentication.git
    cd hospital-rolebased-authentication
    ```

2.  **Install Backend Dependencies:**

    ```bash
    # Example for Python/Django
    cd backend
    pip install -r requirement.txt
    ```

3.  **Install Frontend Dependencies:**
    ```bash
    cd frontend
    ```

### Configuration

1.  **Database Setup:**
    *   Create a database named `hospital_auth` (or as specified in your `config` files).
    *   Update database connection strings in your `config.env` (or equivalent) file.

2.  **Environment Variables:**
    Create a `.env` file in your backend directory and add the following (adjust as per your actual project's needs):
    ```
    PORT=5000
    MONGO_URI=your_mongodb_connection_string
    JWT_SECRET=your_secret_jwt_key
    JWT_LIFETIME=1d
    # Add any other necessary environment variables (e.g., email service credentials)
    ```

### Running the Application

1.  **Start the Backend Server:**
    ```bash
    # Example for Node.js
    cd backend
    npm start
    ```
    ```bash
    # Example for Python/Django
    cd backend
    python manage.py runserver
    ```
    The backend server should now be running on `http://localhost:5000` (or your configured port).

2.  **Start the Frontend Development Server:**
    ```bash
    # Example for React/Angular/Vue
    cd frontend
    npm start
    ```
    The frontend application should open in your browser, typically at `http://localhost:3000`.

## Usage

*   **Admin Access:** Initial setup might require creating an admin user manually in the database or through a specific registration route.
*   **Login:** Users can log in with their credentials. The system will direct them based on their assigned role.
*   **Role-Specific Dashboards:**
    *   **Admin:** Manage users, roles, and system settings.
    *   **Doctor:** Access patient records, update diagnoses, prescribe medications.
    *   **Nurse:** View patient charts, administer treatments, record observations.
    *   **Patient:** View their own medical history, appointments, and billing information.

## API Endpoints (Optional, but recommended for backend projects)

| Endpoint                 | Method | Description                                  | Access Role      |
| :----------------------- | :----- | :------------------------------------------- | :--------------- |
| `/api/auth/register`     | POST   | Register a new user                          | All              |
| `/api/auth/login`        | POST   | Authenticate user and get JWT                | All              |
| `/api/users`             | GET    | Get all users                                | Admin            |
| `/api/users/:id`         | GET    | Get user by ID                               | Admin, Self      |
| `/api/users/:id`         | PUT    | Update user details                          | Admin, Self      |
| `/api/users/:id`         | DELETE | Delete a user                                | Admin            |
| `/api/patients`          | GET    | Get all patient records                      | Admin, Doctor, Nurse |
| `/api/patients/:id`      | GET    | Get a specific patient record                | Admin, Doctor, Nurse, Self (patient) |
| `/api/patients/:id/vitals` | POST   | Add patient vitals                           | Nurse            |
| `/api/doctors`           | GET    | Get list of doctors                          | All (general info) |
| `/api/admin/roles`       | GET/POST | Manage roles and permissions                | Admin            |

## Project Structure (Optional, but helpful)

hospital-rolebased-authentication/
├── backend/
│ ├── config/
│ ├── controllers/
│ ├── models/
│ ├── routes/
│ ├── middleware/
│ ├── server.js
│ ├── package.json (or requirements.txt)
│ └── .env.example
├── frontend/
│ ├── public/
│ ├── src/
│ │ ├── components/
│ │ ├── pages/
│ │ ├── services/
│ │ ├── App.js
│ │ └── index.js
│ └── package.json
└── README.md

## Contributing

Contributions are welcome! If you'd like to improve this project, please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add new feature'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Open a Pull Request.

## License

This project is licensed under the [MIT License](LICENSE).

---
