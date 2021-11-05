# Thank you to: https://github.com/rowdybeaver/sample-django-docker/blob/master/Dockerfile

# Defining arguments before the first FROM makes it global to all stages of the 
# entire Dockerfile
ARG USERNAME=user1

#----- Stage 1: Install dependencies, copy code and create user
FROM python:3.9 AS appbuilder

ARG USERNAME
ARG USERUID=1000
ARG USERGID=1000

# python environment variables
ENV PYTHONDONTWRITEBYTECODE 1
# do not write buffered, because this may lead
# to output not being directly visible in the log
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY build/requirements.txt ./
RUN pip install -r requirements.txt

RUN addgroup --gid $USERGID $USERNAME \
    && adduser --firstuid $USERUID --gid $USERGID \
    --gecos "$USERNAME" --disabled-password $USERNAME

RUN chown ${USERNAME} /app
RUN mkdir /tiles \
    && chown ${USERNAME} /tiles

COPY ./openwastemap/ /app/
ENV PATH="/app:${PATH}"

RUN python -m compileall -q -x '/\.git' .

#----- Stage 2: Become non-root user
FROM appbuilder as applayer

ARG USERNAME

USER ${USERNAME}

#----- Stage 3: Build static content
FROM appbuilder as staticbuilder

RUN export DJANGO_SETTINGS_MODULE="openwastemap.local_settings" \
    && python manage.py collectstatic --no-input

#----- Stage 4: Build nginx web server with static content only
FROM nginx:latest as staticlayer

EXPOSE 80

VOLUME /var/log/nginx
COPY --from=staticbuilder /app/build/static/ /app/build/static/

COPY httpd/ /etc/nginx/conf.d/
