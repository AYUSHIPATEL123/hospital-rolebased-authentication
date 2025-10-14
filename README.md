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

