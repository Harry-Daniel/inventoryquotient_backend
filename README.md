# Inventory Quotient — Backend

REST API for Inventory Quotient, an inventory tracker where each user manages their own items, each with a stock count and a product image.

Built with Django, Django REST Framework, Djoser and Simple JWT. Images are stored on Cloudinary, data in PostgreSQL. Deployed on Render.

## Features

- Email-based user accounts with JWT authentication
- Per-user inventory: users only ever see and edit their own items
- Item names are unique per user (case-insensitive)
- Item and profile images uploaded to Cloudinary, with cleanup if saving fails
- Django admin at `/admin/`

## Tech stack

| Area      | Library                                   |
|-----------|-------------------------------------------|
| Framework | Django 6, Django REST Framework           |
| Auth      | Djoser, djangorestframework-simplejwt     |
| Database  | PostgreSQL via `dj-database-url`          |
| Media     | Cloudinary                                |
| Serving   | Gunicorn, WhiteNoise for static files     |

## Getting started

### Prerequisites

- Python 3.12
- A PostgreSQL database
- A Cloudinary account

### Setup

```bash
git clone https://github.com/Harry-Daniel/inventoryquotient_backend.git
cd inventoryquotient_backend

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Copy the example environment file and fill in your values:

```bash
cp .env.example .env
```

| Variable                 | Description                         |
|--------------------------|-------------------------------------|
| `SECRET_KEY`             | Django secret key                   |
| `DATABASE_URL`           | PostgreSQL connection string        |
| `CLOUDINARY_CLOUD_NAME`  | Cloudinary cloud name               |
| `CLOUDINARY_API_KEY`     | Cloudinary API key                  |
| `CLOUDINARY_API_SECRET`  | Cloudinary API secret               |

Generate a secret key with:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Run migrations and start the server:

```bash
python manage.py migrate
python manage.py runserver
```

> `DEBUG` is `False` and `ALLOWED_HOSTS` only lists the production domain. For local development, set `DEBUG = True` and add `localhost` / `127.0.0.1` to `ALLOWED_HOSTS` in `inventoryquotient_backend/settings.py`.

### Creating a superuser

Either run `python manage.py createsuperuser`, or set these environment variables and run the script (useful on hosts without shell access):

```env
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=a-strong-password
```

```bash
python create_superuser.py
```

## API

Authenticated requests use the `JWT` header prefix:

```
Authorization: JWT <access_token>
```

Access tokens are valid for 1 day.

### Auth

| Method | Endpoint               | Description                                   |
|--------|------------------------|-----------------------------------------------|
| POST   | `/auth/users/`         | Register (`email`, `username`, `first_name`, `last_name`, `password`) |
| POST   | `/auth/jwt/create/`    | Log in with `email` and `password`; returns `access` and `refresh` |
| POST   | `/auth/jwt/refresh/`   | Get a new access token from a `refresh` token |
| POST   | `/auth/jwt/verify/`    | Check that a token is valid                   |
| GET    | `/auth/users/me/`      | Current user's profile                        |
| PATCH  | `/auth/users/me/`      | Update profile; send `profile_image` as multipart to upload a picture |

Other Djoser endpoints (password change, etc.) are also available under `/auth/`.

### Inventory

All endpoints require authentication.

| Method | Endpoint                  | Description                          |
|--------|---------------------------|--------------------------------------|
| GET    | `/inventory/items/`       | List your items, sorted by name      |
| POST   | `/inventory/items/`       | Create an item (multipart, `image` required) |
| GET    | `/inventory/items/{id}/`  | Get one item                         |
| PUT    | `/inventory/items/{id}/`  | Replace an item                      |
| PATCH  | `/inventory/items/{id}/`  | Update some fields                   |
| DELETE | `/inventory/items/{id}/`  | Delete an item                       |

Item fields:

| Field             | Type     | Notes                                   |
|-------------------|----------|-----------------------------------------|
| `id`              | integer  | Read-only                               |
| `name`            | string   | Unique per user                         |
| `description`     | string   |                                         |
| `inventory`       | integer  | Stock count, minimum 0                  |
| `image`           | file     | Write-only upload; stored on Cloudinary |
| `image_url`       | string   | Set by the server after upload          |
| `image_public_id` | string   | Cloudinary ID, set by the server        |
| `last_update`     | datetime | Updated automatically                   |
| `user`            | integer  | Read-only, the owner                    |

When updating, sending a new `image` file replaces the existing image in place. If you send no image, the current one is kept.

Example:

```bash
curl -X POST https://inventoryquotient.onrender.com/inventory/items/ \
  -H "Authorization: JWT $ACCESS_TOKEN" \
  -F name="Widget" \
  -F description="Blue widget, 10cm" \
  -F inventory=25 \
  -F image=@widget.jpg
```

## Deployment

The app is set up for Render (or any host that runs a Procfile):

- Start command: `gunicorn inventoryquotient_backend.wsgi`
- Set `SECRET_KEY`, `DATABASE_URL` and the three `CLOUDINARY_*` variables in the host's environment
- Build step: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`

## Project structure

```
inventoryquotient_backend/   Project settings and root URLs
inventory/                   Item model, serializer and viewset
users/                       Custom User model (email login) and serializers
create_superuser.py          Creates an admin from environment variables
```
