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