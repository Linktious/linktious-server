FROM python:3.9-alpine3.12 AS base
RUN apk add --update build-base alpine-sdk libffi-dev openssl-dev python3-dev 
RUN pip install "cryptography==3.1.1" "poetry==1.1.4"
# Application dependencies
COPY pyproject.toml poetry.lock /app/

WORKDIR /app/
# TODO: use --no-dev for skipping dev dependencies
RUN POETRY_VIRTUALENVS_IN_PROJECT=true poetry install --no-root


FROM python:3.9-alpine3.12
WORKDIR /app/
RUN apk --no-cache add curl
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/src:${PYTHONPATH}"
COPY --from=base /app/ /app/
# Application files
COPY src /app/src/

ARG PORT=8000
ENV PORT ${PORT}
CMD ["sh", "-c", "uvicorn src.app:app --host 0.0.0.0 --port $PORT"]
