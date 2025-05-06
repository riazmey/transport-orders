
#!/bin/sh

python /app/classifiers/manage.py createcachetable

python /app/classifiers/manage.py runserver 0.0.0.0:${WEB_PORT}
#gunicorn server.wsgi --bind 0.0.0.0:8000 --workers 4 --threads 4
#gunicorn /app/classifiers/core/.wsgi --bind 0.0.0.0:${WEB_PORT} --workers 6 --threads 6
