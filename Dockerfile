FROM python:3.13-slim AS build-env
COPY . /app
WORKDIR /app

# hadolint ignore=DL3006
FROM gcr.io/distroless/python3

COPY --from=build-env /app /app
WORKDIR /app
ENTRYPOINT ["bash", "docker-entrypoint.sh"]