# Django Ecommerce API (Demo)

This is a **Django-based e-commerce backend** project, implemented as a **REST API** with Django REST Framework (DRF).  
The project is fully dockerized for **easy local development and demo purposes**, including PostgreSQL as the database.  
It also uses **drf-yasg** for automatic API documentation.

---

## Features

- REST API for an e-commerce platform.
- Models for Users, Products, Categories, Cart, Orders, Reviews, and Payments.
- User authentication and permissions (Admin, Staff, and regular users).
- API documentation via **Swagger / OpenAPI** (`/docs/` endpoint).
- Dockerized backend with PostgreSQL database.
- Ready for demo or development environment without external setup.

---

## Project Structure

ecommerce/
├── apps/
│ ├── users/
│ ├── products/
│ ├── cart/
│ ├── orders/
│ ├── payments/
│ └── reviews/
├── ecommerce/ # Django project settings
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── requirements.txt
├── .env.example


---

## Prerequisites

- Docker >= 24.x
- Docker Compose >= 2.x

> No local installation of Python or PostgreSQL is required. Everything runs in containers.

---

## Getting Started

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <repo-folder>

2. Copy environment variables

cp .env.example .env

Edit .env if you want to change database credentials or Django secret key.
3. Build and start Docker containers

docker compose up --build

This command will:

    Build the Docker image for Django.

    Start PostgreSQL database container.

    Wait until the database is ready.

    Apply Django migrations.

    Start the development server on http://localhost:8000/.

4. Access the API

    Swagger / OpenAPI docs:
    http://localhost:8000/docs/

    Development server:
    http://localhost:8000/

    If you want to stop containers:

docker compose down -v

Docker Notes

    The entrypoint.sh script ensures the database is ready before Django starts.

    DJANGO_ENV=development in .env runs the Django development server for demo purposes.

    gunicorn is configured for production but not used in demo mode.

API Overview

    Users: CRUD operations, authentication.

    Products & Categories: Manage catalog items.

    Cart & Cart Items: Add/remove products in user carts.

    Orders: Create, list, and manage orders.

    Payments: Record payment information.

    Reviews: Users can add reviews to products.

    All API endpoints are documented in Swagger UI (/docs/).

Contributing

This project is intended as a demo backend. You can:

    Fork the repository.

    Modify/add apps or models.

    Add serializers, views, and permissions.

    Test locally with Docker.

License

This project is for demo and portfolio purposes.
