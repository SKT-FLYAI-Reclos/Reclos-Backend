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

#### User Login

```http
  POST api/user/login/
```

Allows users to log in and obtain authentication credentials.

| Parameter  | Type     | Description                          |
| :--------- | :------- | :----------------------------------- |
| `username` | `string` | **Required**. Your registered username |
| `password` | `string` | **Required**. Your password          |

#### User Logout

```http
  POST api/user/logout/
```

Logs out the current authenticated user.

#### Password Change

```http
  POST api/user/password/change/
```

Allows an authenticated user to change their password.

| Parameter       | Type     | Description                            |
| :-------------- | :------- | :------------------------------------- |
| `new_password1` | `string` | **Required**. The new password         |
| `new_password2` | `string` | **Required**. Confirmation of the new password |

#### Password Reset

```http
  POST api/user/password/reset/
```

Initiates a password reset process for a user.

| Parameter  | Type     | Description                       |
| :--------- | :------- | :-------------------------------- |
| `email`    | `string` | **Required**. Email of the user to reset the password for |

#### Password Reset Confirm

```http
  POST api/user/password/reset/confirm/
```

Completes the password reset process.

| Parameter        | Type     | Description                              |
| :--------------- | :------- | :--------------------------------------- |
| `uid`            | `string` | **Required**. The user's ID encoded in base64 |
| `token`          | `string` | **Required**. The password reset token   |
| `new_password1`  | `string` | **Required**. The new password           |
| `new_password2`  | `string` | **Required**. Confirmation of the new password |

#### User Signup

```http
  POST api/user/signup/
```

Registers a new user to the application.

| Parameter   | Type     | Description                            |
| :---------- | :------- | :------------------------------------- |
| `username`  | `string` | **Required**. Desired username         |
| `email`     | `string` | **Required**. User's email address     |
| `password1` | `string` | **Required**. Password                 |
| `password2` | `string` | **Required**. Password confirmation    |

#### Token Verification

```http
  POST api/user/token/verify/
```

Verifies a token obtained from the login endpoint.

| Parameter | Type     | Description                            |
| :-------- | :------- | :--------------------------------
| `token`   | `string` | **Required**. The token to verify      |

#### Token Refresh

```http
  POST api/user/token/refresh/
```

Obtains a new access token using a refresh token.

| Parameter      | Type     | Description                            |
| :------------- | :------- | :------------------------------------- |
| `refresh`      | `string` | **Required**. The refresh token        |


These endpoints are provided by `dj-rest-auth` and handle various aspects of user authentication, registration, and account management. The actual behavior and requirements of each endpoint might vary depending on the configuration of `dj-rest-auth` and your Django project settings.