Python 3.11.5

# Setup

#### Venv
```
python -m venv .venv
.venv\Scripts\activate
```

#### Install
```
pip install -r requirements.txt
```

#### Create DB Schema
In mysql, create schema "reclos"

#### Create .env
Copy .env.example to .env and fill in the values

#### Run Server
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

# API Reference

## User

### Get User(s)

```http
GET /api/user/
GET /api/user/<int:id>/
```

Retrieves all users or a specific user by ID.

No parameters required for listing all users. For retrieving a specific user, the user ID is part of the URL path.

### User Login

```http
POST /api/user/login/
```

Allows users to log in and obtain authentication credentials.

| Parameter  | Type     | Description                      |
|------------|----------|----------------------------------|
| `username` | `string` | **Required**. Registered username |
| `password` | `string` | **Required**. Password           |

### User Logout

```http
POST /api/user/logout/
```

Logs out the current authenticated user.

### Password Change

```http
POST /api/user/password/change/
```

Allows an authenticated user to change their password.

| Parameter       | Type     | Description                        |
|-----------------|----------|------------------------------------|
| `new_password1` | `string` | **Required**. New password         |
| `new_password2` | `string` | **Required**. Confirmation of new password |

### Password Reset

```http
POST /api/user/password/reset/
```

Initiates a password reset process for a user. (Not working)

| Parameter  | Type     | Description                           |
|------------|----------|---------------------------------------|
| `email`    | `string` | **Required**. Email for password reset |

### Password Reset Confirm

```http
POST /api/user/password/reset/confirm/
```

Completes the password reset process.

| Parameter        | Type     | Description                          |
|------------------|----------|--------------------------------------|
| `uid`            | `string` | **Required**. User's ID (base64 encoded) |
| `token`          | `string` | **Required**. Password reset token   |
| `new_password1`  | `string` | **Required**. New password           |
| `new_password2`  | `string` | **Required**. Confirmation of new password |

### User Signup

```http
POST /api/user/signup/
```

Registers a new user to the application.

| Parameter   | Type     | Description                    |
|-------------|----------|--------------------------------|
| `username`  | `string` | **Required**. Desired username |
| `email`     | `string` | **Required**. Email address    |
| `password1` | `string` | **Required**. Password         |
| `password2` | `string` | **Required**. Password confirmation |

### Token Verification

```http
POST /api/user/token/verify/
```

Verifies a token obtained from the login endpoint.

| Parameter | Type     | Description                  |
|-----------|----------|------------------------------|
| `token`   | `string` | **Required**. Token to verify |

### Token Refresh

```http
POST /api/user/token/refresh/
```

Obtains a new access token using a refresh token.

| Parameter | Type     | Description                    |
|-----------|----------|--------------------------------|
| `refresh` | `string` | **Required**. Refresh token    |


### Initiate Kakao Login

To start the Kakao login process, direct the user to the following URL:

```url
https://kauth.kakao.com/oauth/authorize?client_id=<KAKAO_REST_API_KEY>&redirect_uri=<REDIRECT_URI>&response_type=code
```

Replace `<KAKAO_REST_API_KEY>` with your Kakao REST API Key and `<REDIRECT_URI>` with the URI where you want Kakao to send the response (this should match the one configured in your Kakao application settings). The user will be prompted to log in to Kakao and authorize your application.

### Kakao Login

After the user logs in and authorizes the application, Kakao will redirect them to your specified `redirect_uri` with a `code` query parameter. Use this code to complete the login process:

```http
GET /api/user/kakao/login/?code=<code>
```

This endpoint on your server should handle the code exchange for an access token and retrieve the user's information from Kakao.

| Parameter | Type     | Description                                  |
|-----------|----------|----------------------------------------------|
| `code`    | `string` | **Required**. Code provided by Kakao after user login |

On success, this endpoint returns JWT tokens (`access` and `refresh`) along with the user's basic information.



## Board
