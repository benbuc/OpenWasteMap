FROM python:3.10 AS base

WORKDIR /app/

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./app/pyproject.toml ./app/poetry.lock* /app/

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --only main ; fi"

# For development, Jupyter remote kernel, Hydrogen
# Using inside the container:
# jupyter lab --ip=0.0.0.0 --allow-root --NotebookApp.custom_display_url=http://127.0.0.1:8888
ARG INSTALL_JUPYTER=false
RUN bash -c "if [ $INSTALL_JUPYTER == 'true' ] ; then pip install jupyterlab ; fi"

FROM base AS celeryworker

ENV C_FORCE_ROOT=1

COPY ./app /app
WORKDIR /app

ENV PYTHONPATH=/app

COPY ./app/worker-start.sh /worker-start.sh

RUN chmod +x /worker-start.sh

CMD ["bash", "/worker-start.sh"]

FROM base AS backend

COPY ./app/backend-start-reload.sh /
COPY ./app/backend-start.sh /
RUN chmod +x /backend-start-reload.sh
RUN chmod +x /backend-start.sh
COPY ./app /app
ENV PYTHONPATH=/app

CMD ["bash", "/backend-start.sh"]

FROM base AS tile_manager

COPY ./app/tile-manager-start-reload.sh /
COPY ./app/tile-manager-start.sh /
RUN chmod +x /tile-manager-start-reload.sh
RUN chmod +x /tile-manager-start.sh
COPY ./app /app
ENV PYTHONPATH=/app

CMD ["bash", "/tile-manager-start.sh"]