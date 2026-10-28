# Inventory Quotient — Backend

REST API for Inventory Quotient, an inventory tracker where each user manages their own items, each with a stock count and a product image.

Built with Django, Django REST Framework, Djoser and Simple JWT. Images are stored on Cloudinary, data in PostgreSQL.

> **Note:** This backend was deployed on Render at `https://inventoryquotient.onrender.com`. That link no longer works: the app ran on a free-tier database instance, which is now down.

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

## Deployment

The project is configured for production on Render:

- `DEBUG` is `False`, and `ALLOWED_HOSTS` only allows `inventoryquotient.onrender.com`
- The database connection comes from `DATABASE_URL` (PostgreSQL)
- Static files are collected into `staticfiles/` and served by WhiteNoise
- The app runs under Gunicorn, as set in the `Procfile`:

  ```
  web: gunicorn inventoryquotient_backend.wsgi
  ```

### Environment variables

These are set in the host's environment. `.env.example` lists them all, and `settings.py` also loads a `.env` file if one exists.

| Variable                    | Description                          |
|-----------------------------|--------------------------------------|
| `SECRET_KEY`                | Django secret key                    |
| `DATABASE_URL`              | PostgreSQL connection string         |
| `CLOUDINARY_CLOUD_NAME`     | Cloudinary cloud name                |
| `CLOUDINARY_API_KEY`        | Cloudinary API key                   |
| `CLOUDINARY_API_SECRET`     | Cloudinary API secret                |
| `DJANGO_SUPERUSER_EMAIL`    | Admin email, for `create_superuser.py` |
| `DJANGO_SUPERUSER_USERNAME` | Admin username                       |
| `DJANGO_SUPERUSER_PASSWORD` | Admin password                       |

### Build and start

```bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
python create_superuser.py   # creates the admin from the DJANGO_SUPERUSER_* variables, if it doesn't exist yet
gunicorn inventoryquotient_backend.wsgi
```

To deploy it under a different domain, add that domain to `ALLOWED_HOSTS` in `inventoryquotient_backend/settings.py`.

## Project structure

```
inventoryquotient_backend/   Project settings and root URLs
inventory/                   Item model, serializer and viewset
users/                       Custom User model (email login) and serializers
create_superuser.py          Creates an admin from environment variables
```
