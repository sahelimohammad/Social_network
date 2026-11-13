# Social Network

A Django social networking website with user profiles, posts, reactions, comments, following, and real-time chat rooms.

[فارسی — README.fa.md](README.fa.md)

## Features

- Account registration, login, profile editing, and password reset
- Posts with text and images; post editing and deletion
- Comments, replies, likes, and dislikes
- Following and unfollowing users
- Searching posts by text
- Real-time chat rooms using WebSockets and Django Channels
- Chat messages saved in SQLite, with Redis used for the channel layer

## Technology

Python · Django · Django Channels · Daphne · Redis · SQLite · Django REST Framework · HTML/CSS/JavaScript

## Project structure

```text
account/          Authentication and user profiles
home/             Posts, comments, reactions, search and following
chat/             Chat rooms, messages and WebSocket consumer
pr2/              Django configuration, routing, ASGI/WSGI
templates/        Shared page templates
manage.py         Django management commands
requirements.txt  Python dependencies
.env.example      Local environment-variable template
```

## Local installation

Python 3.12 and a running Redis server on `localhost:6379` are recommended for this project.

### 1. Create a virtual environment

Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Linux/macOS:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### 2. Configure the application

Create a file named `.env` in the project root by copying `.env.example` and set a unique `DJANGO_SECRET_KEY`:

```powershell
Copy-Item .env.example .env
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Paste the generated key into `.env`, replacing `replace-with-a-long-random-secret-key`. Email credentials are optional for local use; without them, password-reset emails appear in the terminal.

### 3. Start Redis

If Docker is available:

```bash
docker run --name social-network-redis -p 6379:6379 -d redis:7
```

If the container already exists but is stopped, use `docker start social-network-redis` instead. Redis is needed for WebSocket chat; the standard Django pages can be explored without using chat.

### 4. Prepare the database and launch

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open <http://127.0.0.1:8000/home/>. You can also register a regular account at `/account/register/`. Chat rooms are available under `/chat/` after login.

### 5. Run tests

```bash
python manage.py check
python manage.py test tests
```

## Development notes

- SQLite is used for local development; `db.sqlite3` is created by migrations and is not included in the repository.
- Uploaded images and user content are stored under `media/`, which is excluded from version control.
- Redis should be running for real-time chat functionality.
- The repository contains application source and migrations, but no user accounts or chat history.
- WebSocket room access and message-author validation need further hardening before public deployment. The current implementation is intended for local demonstration, not a production messaging service.
- The included Django 4.2 branch is no longer supported. Upgrade to a supported Django version and retest before production deployment.

## Static assets

The project includes frontend assets used by its templates. Check the licenses and attribution requirements of third-party themes and images before redistributing them outside this project.
