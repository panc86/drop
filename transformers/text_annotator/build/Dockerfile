ARG REGISTRY=index.docker.io
FROM $REGISTRY/python:3.10.6-slim AS base



# =======================================
# STAGE builder
#
# Builds the Python virtual environment
# ======================================= 
FROM base AS builder

# proxy
ARG http_proxy
ARG https_proxy

# system env
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_NO_INTERACTION=1
ENV PATH="$POETRY_HOME/bin:$PATH"

# install poetry
RUN apt update && \
    apt install -y --no-install-recommends curl

# setup workspace
WORKDIR /usr/src/app
COPY pyproject.toml .

# install virtual env
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    poetry install --no-cache --compile --only main

# copy source code
COPY src ./src



# =======================================
# STAGE production
#
# Build the production docker image with
# only required components i.e. source
# code and virtual environment
# ======================================= 
FROM base AS production
COPY --from=builder /usr/src/app /usr/src/app

WORKDIR /usr/src/app
ENV PATH="/usr/src/app/.venv/bin:$PATH"

# reduce TensorFlow verbosity
ENV TRANSFORMERS_VERBOSITY=error
ENV TF_CPP_MIN_LOG_LEVELv=3

# volume for annotation models
VOLUME /usr/src/app/src/annotation/data 

ENTRYPOINT ["./src/entrypoint.sh"]
CMD ["--help"]
