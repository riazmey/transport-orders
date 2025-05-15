
#!/bin/sh

python /app/transport-orders/manage.py createcachetable

python /app/transport-orders/manage.py runserver 0.0.0.0:${WEB_PORT}
#gunicorn server.wsgi --bind 0.0.0.0:8000 --workers 4 --threads 4
#gunicorn /app/transport-orders/core/.wsgi --bind 0.0.0.0:${WEB_PORT} --workers 6 --threads 6
