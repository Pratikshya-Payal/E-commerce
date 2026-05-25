# Django E-Commerce Website

This repository contains a complete Django-based E-Commerce web application.

---

## Project Features

- User Registration & Login
- Product Listing
- Product Details Page
- Shopping Cart
- Checkout System
- Order Management
- Admin Dashboard
- Responsive Design using Bootstrap
- Product Image Upload
- SQLite Database

---

## Project Structure

- `core/` - Main Django project folder
  - `manage.py` - Django management script
  - my_shop/` - Main project package
    - `settings.py` - Project settings
    - `urls.py` - URL routing
    - `wsgi.py` - WSGI configuration
    - `asgi.py` - ASGI configuration

- `store/` - Main E-Commerce application
  - `models.py` - Database models
  - `views.py` - Application views
  - `urls.py` - App URLs
  - `forms.py` - Django forms
  - `admin.py` - Admin configuration
  - `templates/` - HTML templates
  - `static/` - CSS, JavaScript, and Images
  - `migrations/` - Database migrations

- `media/` - Uploaded product images
- `db.sqlite3` - SQLite database
- `requirements.txt` - Project dependencies

---

## Setup Instructions

### 1. Clone the Repository

```powershell
git clone https://github.com/your-username/django-ecommerce.git
