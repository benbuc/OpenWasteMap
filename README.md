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
# Remember the empty line at the end of the cron file
```
The last command removes successfull log entries older than a week.

## Local Settings
We are using `local_settings.py` like discussed here:
https://stackoverflow.com/questions/4909958/django-local-settings

In the production and development environment the default settings should be overwritten.
Add settings to `openwastemap/openwastemap/local_settings.py`.
The minimal configuration can look like this:

```python
from .settings import *

SECRET_KEY = "not_a_secret"

STATIC_ROOT = "/app/build/static"
TILES_ROOT = "/tiles"

DATABASES = {
   "default": {
      "ENGINE": "django.db.backends.mysql",
      "NAME": "database_name",
      "USER": "username",
      "PASSWORD": "password",
      "HOST": "host.docker.internal",
      "PORT": 3306,
   }
}

ALLOWED_HOSTS = ["add.the.host"]

EMAIL_HOST = "mail.host.net"
EMAIL_SERVER = "mail.host.net"
EMAIL_HOST_PASSWORD = "password"
EMAIL_PASSWORD = "password"
EMAIL_HOST_USER = "user@name.net"
EMAIL_ADDRESS = "user@name.net"
DEFAULT_FROM_EMAIL = "noreply@thedomain.net"
EMAIL_FROM_ADDRESS = "noreply@thedomain.net"
EMAIL_PAGE_DOMAIN = "http://add.the.host/"
```

### Debug
In a debug environment, add the following flag to show django error messages and other debug information.
```python
DEBUG = True
```

### Disable Tile Caching
Normally, OWM is saving all rendered tiles to disk and using these if requested.
When debugging the rendering it could therefore be necessary to disable this behaviour.
```python
CHECK_TILE_CACHE_HIT = False
```

### Profiling with Silk
To enable profiling with [silk](https://github.com/jazzband/django-silk), add the following:
```python
SILKY_PYTHON_PROFILER = True
INSTALLED_APPS += ["silk"]
MIDDLEWARE += ["silk.middleware.SilkyMiddleware"]
```
The profiler can then be accessed under `/silk`.

### Trusted Origins
When using an internal proxy on the server, the host differs from the CSRF origin.
To allow the other origin use: [CSRF_TRUSTED_ORIGINS](https://docs.djangoproject.com/en/3.2/ref/settings/#csrf-trusted-origins)