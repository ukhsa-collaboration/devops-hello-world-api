from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class HelloWorldTest(TestCase):
    def test_hello_world_json(self):
        url = reverse("hello")
        response = self.client.get(url)
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {"message": "Hello, world!"}
