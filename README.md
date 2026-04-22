# Inventory Management System - Backend

Django REST Framework backend for Inventory Management System.

## Setup

1. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Create superuser:
```bash
python manage.py createsuperuser
```

5. Run server:
```bash
python manage.py runserver
```

## API Endpoints

### Authentication
- POST `/api/auth/register/` - Register new user
- POST `/api/auth/login/` - Login
- GET `/api/auth/me/` - Get current user

### Products
- GET/POST `/api/products/` - List/Create products
- GET/PUT/DELETE `/api/products/{id}/` - Product detail
- GET `/api/products/low_stock/` - Low stock products

### Inventory
- GET `/api/inventory/` - List inventory
- GET `/api/inventory/summary/` - Inventory summary

### Stock
- GET/POST `/api/stock/movements/` - Stock movements
- GET/POST `/api/stock/cycle-counts/` - Cycle counts
- GET/POST `/api/stock/restock-requests/` - Restock requests
"# Sari-Sari-Store-IMS-backend" 
