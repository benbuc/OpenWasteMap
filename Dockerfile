ARG USERNAME=user1

FROM python:3.9 AS appbuilder

ARG USERNAME
ARG USERUID=1000
ARG USERGID=1000

WORKDIR /app

RUN addgroup --gid $USERGID $USERNAME \
    && adduser --firstuid $USERUID --gid $USERGID \
    --gecos "$USERNAME" --disabled-password $USERNAME

USER ${USERNAME}

ENV PATH="/home/${USERNAME}/.local/bin:${PATH}"

COPY build/requirements.txt ./
RUN pip install -r requirements.txt
COPY ./owm/ /app/
ENV PYTHONPATH=/app
ENV PATH="/app:${PATH}"

FROM appbuilder as applayer

ARG USERNAME

USER ${USERNAME}

FROM appbuilder as staticbuilder

RUN export SECRET_KEY=x \
    && python manage.py collectstatic --no-input -v0 \
    && echo "Static filesystem populated"

FROM nginx:latest as staticlayer

EXPOSE 80

VOLUME /var/log/nginx
COPY --from=staticbuilder /app/static/ /app/static/

COPY httpd/ /etc/nginx/conf.d/
