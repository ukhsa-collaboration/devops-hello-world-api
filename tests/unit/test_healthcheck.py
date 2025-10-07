from http import HTTPStatus

from django.test import TestCase


class HealthCheckMiddlewareTest(TestCase):
    def test_health_endpoint_returns_ok(self):
        response = self.client.get("/health")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == {"status": "ok"}
