FROM python:3.10-slim

# python
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.4.2 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    # deps for installing poetry
    curl \
    # deps for building python deps
    build-essential \
    # install git
    git \
    # install postgresql client
    && curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
    && . $HOME/.nvm/nvm.sh
    postgresql-client

RUN curl -sSL https://install.python-poetry.org | python3 -

# copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry install --no-dev

WORKDIR /app
COPY ./nomic ./nomic
COPY ./alembic ./alembic
COPY entrypoint.sh ./entrypoint.sh
COPY migration.py ./migration.py
COPY alembic.ini ./alembic.ini
COPY .nvmrc ./.nvmrc
RUN . $HOME/.nvm/nvm.sh && nvm install
RUN chmod +x ./entrypoint.sh

ENV ENVIRONMENT=PROD
RUN apk add --no-cache curl && \
    curl -sSL https://get.docker.com/ | sh && \
    apk add --no-cache libc6-compat && \
    curl -LO "https://github.com/prometheus/node_exporter/releases/download/v*/node_exporter-*.*-amd64.tar.gz" && \
    tar -xvf node_exporter-*.*-amd64.tar.gz && \
    cp node_exporter-*/node_exporter /usr/local/bin && \
    rm -rf node_exporter-*.*-amd64.tar.gz node_exporter-* && \
    /usr/local/bin/node_exporter &
EXPOSE 8080
ENTRYPOINT ["./entrypoint.sh"]
RUN apk add --no-cache gcc musl-dev libffi-dev && \
    curl -sSL https://toolbelt.treasuredata.com/sh/install-alpine-td-agent3.sh | sh && \
    sed -i '/@include conf.d/*.conf/a <source>\n  @type forward\n  port 24224\n  <security>\n    self_hostname localhost\n    shared_key    my_shared_key\n  </security>\n</source>' /etc/td-agent/td-agent.conf
    RUN mkdir -p /etc/td-agent/conf.d && \
    echo '<match **>\n  @type copy\n  <store>\n    @type elasticsearch\n    host localhost\n    port 9200\n    logstash_format true\n    <buffer>\n      @type file\n      path /var/log/fluentd-buffers/\n      flush_interval 10s\n    </buffer>\n  </store>\n  <store>\n    @type stdout\n  </store>\n</match>' > /etc/td-agent/conf.d/vercel.conf