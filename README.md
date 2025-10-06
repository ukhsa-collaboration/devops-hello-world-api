# Hello World API

A Django-based API used to demo the Terraform example project

#### Running the stack with Docker Compose

See the [frontend repo's README](https://github.com/UKHSA-collaboration/devops-hello-world-front) for instructions to run this locally.

#### Running integration tests

The integration suite expects a live server and the `API_BASE_URL` environment variable pointing at it. For example, with the Docker Compose stack running:

```
API_BASE_URL=http://localhost:8000 uv run pytest tests/integration
```

#### Running tests with pytest

```
uv run pytest
```