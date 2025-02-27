FROM python:3.13-slim AS python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


FROM python-base AS builder-base

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    build-essential

ENV POETRY_VERSION=1.8.3
RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR $PYSETUP_PATH
COPY . .

RUN poetry install --no-dev
RUN poetry build


FROM python-base AS development

COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH


WORKDIR $PYSETUP_PATH
RUN poetry install

WORKDIR /app
COPY . .

CMD ["actual_discord_bot/bot.py"]


FROM python-base AS production

COPY --from=builder-base $VENV_PATH $VENV_PATH
COPY --from=builder-base $PYSETUP_PATH/dist .
RUN pip install *.whl

WORKDIR /app


# CMD ["/docker-entrypoint.sh"]
