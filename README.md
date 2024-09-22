# Compound Manager Backend

This is the backend for the Compound Manager web application. It is built using Django and Django REST framework. The backend allows users to create, view, update, delete, and share compounds identified by their SMILES string. Users can register, log in, and authenticate using JWT tokens.

## Features

- **User Authentication**: Registration, login, and token-based authentication using JWT.
- **CRUD Operations**: Create, view, update, and delete compounds.
- **Compound Sharing**: Share compounds with other users.
- **Compound Search**: Search for compounds by their name or SMILES.
- **Expiration Time**: Set expiration time for shared compounds.
- **Audit Logs**: Track creation, updates, and deletion of compounds with timestamps.
- **Analytics**: (Optional) Collect summary data about compound usage.

## Requirements

- Python 3.8+
- Django 4.0+
- Django REST Framework
- Django Simple JWT (for token-based authentication)
- SQLite (default, but can be replaced with any other DB engine)

## Installation

1. **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/compound-manager-backend.git
    cd compound-manager-backend
    ```

2. **Create and Activate a Virtual Environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure Environment Variables**
    Create a `.env` file in the project root directory with the following variables:
    ```bash
    SECRET_KEY=your_secret_key_here
    DEBUG=True
    ```

5. **Apply Migrations**
    ```bash
    python manage.py migrate
    ```

6. **Create Superuser**
    ```bash
    python manage.py createsuperuser
    ```

7. **Run the Server**
    ```bash
    python manage.py runserver
    ```

8. **Access the Admin Panel**
    Go to `http://127.0.0.1:8000/admin` to log in with the superuser credentials.

## API Endpoints

### User Authentication

- **Register**: POST `/api/register/`
    ```json
    {
      "username": "your_username",
      "password": "your_password"
    }
    ```
    Response:
    ```json
    {
      "message": "User registered successfully"
    }
    ```

- **Login**: POST `/api/token/`
    ```json
    {
      "username": "your_username",
      "password": "your_password"
    }
    ```
    Response:
    ```json
    {
      "access": "your_jwt_token",
      "refresh": "your_refresh_token"
    }
    ```

### Compound Operations

- **List Compounds**: GET `/api/compounds/`
- **Create Compound**: POST `/api/compounds/`
    ```json
    {
      "name": "Water",
      "smiles": "O"
    }
    ```

- **Update Compound**: PATCH `/api/compounds/<id>/`
    ```json
    {
      "name": "New Compound Name"
    }
    ```

- **Delete Compound**: DELETE `/api/compounds/<id>/`
- **Share Compound**: POST `/api/compounds/share/`
    ```json
    {
      "recipient_username": "another_user",
      "compound_id": "compound-id-here"
    }
    ```

### Search Compounds

- **Search Compound**: GET `/api/compounds/search/?q=search-term`

### JWT Token Refresh

- **Refresh Token**: POST `/api/token/refresh/`
    ```json
    {
      "refresh": "your_refresh_token"
    }
    ```

## Authentication

Authentication is handled using JWT (JSON Web Token). After logging in, include the token in the `Authorization` header for protected routes:

```
Authorization: Bearer <your_access_token>
```

## Admin Panel

The Django admin panel allows you to manage users, compounds, and shared compounds.

- URL: `http://127.0.0.1:8000/admin`
- Log in using the superuser credentials created earlier.

## Audit Logs

Audit logs for compound creation, updating, and deletion are automatically tracked using `django-auditlog`. You can view the logs in the admin panel.

## Database

By default, this project uses SQLite for local development. You can change the database configuration in `settings.py` to use PostgreSQL, MySQL, or any other database.

## Running Tests

To run tests, use the following command:

```bash
python manage.py test
```
