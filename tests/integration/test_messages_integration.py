"""Integration tests that exercise the message endpoints via HTTP."""

from __future__ import annotations

import os
from urllib.parse import urljoin

import pytest
import requests


@pytest.fixture(scope="session")
def api_base_url() -> str:
    base_url = os.environ.get("API_BASE_URL")
    if not base_url:
        pytest.skip(
            "API_BASE_URL environment variable must be set for integration tests",
        )
    return base_url.rstrip("/")


def test_list_messages_contains_default_message(api_base_url: str) -> None:
    response = requests.get(f"{api_base_url}/v1/message", timeout=5)
    assert response.status_code == 200  # noqa: PLR2004
    payload = response.json()
    assert isinstance(payload, list)
    assert {"message": "Hello, world!"} in payload


def test_create_message_and_fetch_detail(api_base_url: str) -> None:
    create_payload = {"message": "Integration test message"}
    create_response = requests.post(
        f"{api_base_url}/v1/message",
        json=create_payload,
        timeout=5,
    )
    assert create_response.status_code == 201  # noqa: PLR2004
    assert create_response.json() == create_payload

    location = create_response.headers.get("Location")
    assert location, "Location header missing from create response"

    detail_url = urljoin(f"{api_base_url}/", location.lstrip("/"))
    detail_response = requests.get(detail_url, timeout=5)
    assert detail_response.status_code == 200  # noqa: PLR2004
    assert detail_response.json() == create_payload
