# Backend - Elshinta Chat Internal

Instructions to run backend locally. See project README for full guide.

Install dependencies:

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create `.env` from `.env.example` and configure MySQL.

Run migrations:

```
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

WebSocket (Channels) will run on the same `runserver` with ASGI.

Cleanup command:

```
python manage.py cleanup_old_messages
```
