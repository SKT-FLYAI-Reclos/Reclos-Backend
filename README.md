Python 3.11.5

# Setup

## Venv
```
python -m venv .venv
.venv\Scripts\activate
```

## Install
```
pip install -r requirements.txt
```

## Create DB Schema
In mysql, create schema "reclos"

## Create .env
Copy .env.example to .env and fill in the values

# Run Server
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```






# API Endpoints

#### Root Endpoint

```http
  GET /
```

Returns a simple message indicating that the Reclos Backend is running.

| Response           | Type     | Description                       |
| :----------------- | :------- | :-------------------------------- |
| `message`          | `string` | Confirmation that the server is running |

#### Admin Interface

```http
  GET /admin/
```

Access the Django Admin interface for backend management.

#### User Login

```http
  POST /login/
```

Obtain JWT (JSON Web Token) for authenticated access.

| Parameter  | Type     | Description                          |
| :--------- | :------- | :----------------------------------- |
| `username` | `string` | **Required**. Your username          |
| `password` | `string` | **Required**. Your password          |

#### Token Refresh

```http
  POST /refresh/
```

Refresh JWT access token using a refresh token.

| Parameter  | Type     | Description                           |
| :--------- | :------- | :------------------------------------ |
| `refresh`  | `string` | **Required**. Your refresh token      |

#### User Signup

```http
  POST /signup/
```

Register a new user.

| Parameter   | Type     | Description                          |
| :---------- | :------- | :----------------------------------- |
| `username`  | `string` | **Required**. Desired username       |
| `email`     | `string` | **Required**. User's email address   |
| `password1` | `string` | **Required**. Password               |
| `password2` | `string` | **Required**. Password confirmation  |

#### Authentication Management

```http
  /auth/
```

Additional endpoints provided by `dj-rest-auth` for authentication management (password reset, logout, etc.). The exact functionalities depend on the `dj-rest-auth` configuration.

#### User Management

```http
  /api/user/
```

Endpoints for user-specific actions and data management. Details depend on the implementation in `user.urls`.