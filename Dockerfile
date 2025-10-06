FROM python:3.11-slim AS build-env

WORKDIR /app

# hadolint ignore=DL3008,DL4006
RUN apt-get update \
    && apt-get install --no-install-recommends -y curl \
    && rm -rf /var/lib/apt/lists/*  \ 
    && curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:/root/.cargo/bin:${PATH}"

COPY . .

RUN uv sync --frozen --no-dev

RUN ls -la /app

# hadolint ignore=DL3006
FROM gcr.io/distroless/python3:nonroot

WORKDIR /app

COPY --from=build-env /app/.venv /env
COPY --from=build-env /app /app

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/env/bin:/usr/local/bin:${PATH}"
ENV PYTHONPATH="/env/lib/python3.11/site-packages/"

CMD ["run.py"]