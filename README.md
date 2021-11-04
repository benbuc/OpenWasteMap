# OpenWasteMap

## Development Setup

1. Install [poetry](https://github.com/python-poetry/poetry)
   ```bash
   curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
   ```
1. Install the dependencies
   ```bash
   poetry install
   ```
1. Install the [pre-commit](https://github.com/pre-commit/pre-commit) and pre-push hooks
   ```bash
   pre-commit install
   pre-commit install -t pre-push
   ```

### Development Server

Start the development server with
```bash
python manage.py runserver
```

### Development Server Docker
More information on the dockerization I used:
https://github.com/rowdybeaver/sample-django-docker

The Docker Dev Set-up can be launched using
```bash
./build_docker_dev.sh
docker-compose --file docker-compose.dev.yml up
```

## Installing new version on server (No Docker)
```bash
poetry install --no-dev
python manage.py migrate
python manage.py collectstatic
```

## Installing new version on server (Docker)
```bash
docker-compose -f docker-compose.prod.yml down
git pull
./build_docker_prod.sh
docker-compose -f docker-compose.prod.yml up -d
```

## Email sending on server
To prevent email [enumeration timing attacks](https://docs.djangoproject.com/en/3.1/topics/auth/default/#django.contrib.auth.views.PasswordResetView) we are using `django-mailer` for queueing emails and sending them asynchronously.

[https://github.com/pinax/django-mailer/](https://github.com/pinax/django-mailer/)

To automatically send queued emails, this has to be added for example to the crontab:
```
*       * * * * (/path/to/your/python /path/to/your/manage.py send_mail >> ~/cron_mail.log 2>&1)
0,20,40 * * * * (/path/to/your/python /path/to/your/manage.py retry_deferred >> ~/cron_mail_deferred.log 2>&1)
0       0 * * * (/path/to/your/python /path/to/your/manage.py purge_mail_log 7 >> ~/cron_mail_purge.log 2>&1)
```
The last command removes successfull log entries older than a week.