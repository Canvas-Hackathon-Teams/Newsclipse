web: gunicorn --preload --log-file - newsclipse.manage:app
dev: python newsclipse/manage.py runserver
worker: celery -A newsclipse.queue worker
