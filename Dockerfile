FROM python:3.11 as base

ENV PROJECT_NAME="one-more-backend"

ARG APP_HOME="/opt/$PROJECT_NAME"
ARG APP_PORT="8000"
ARG USERNAME="backend"
ENV APP_HOME=${APP_HOME} \
    APP_PORT=${APP_PORT} \
    USERNAME=${USERNAME}

COPY poetry.lock pyproject.toml ./

LABEL application="one-more-backend" \
    author="Sergei Solovev <takentui@gmail.com>"

RUN apt-get update && \
    apt-get install -qy --no-install-recommends build-essential && \
    pip install --no-cache-dir --upgrade pip poetry==1.3.1 && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-root && \
    apt-get remove -qy --purge build-essential && \
    apt-get autoremove -qqy --purge && \
    apt-get clean && \
    rm -rf /var/cache/* poetry.lock pyproject.toml

WORKDIR ${APP_HOME}


FROM base as fastapi

COPY entrypoint-fastapi.sh /usr/local/bin

EXPOSE ${APP_PORT}
ENTRYPOINT ["entrypoint-fastapi.sh"]
CMD ["start"]


FROM base as django

COPY entrypoint-django.sh /usr/local/bin

WORKDIR ./myproject
EXPOSE ${APP_PORT}
ENTRYPOINT ["entrypoint-django.sh"]
CMD ["start"]
