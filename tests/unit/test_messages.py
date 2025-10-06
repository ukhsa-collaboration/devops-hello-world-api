import json
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from hello_world_api import views as message_views


class HelloWorldTest(TestCase):
    def setUp(self):
        message_views._MESSAGES.clear()  # noqa: SLF001
        message_views._MESSAGES.update({1: "Hello, world!"})  # noqa: SLF001
        message_views._NEXT_MESSAGE_ID = 2  # noqa: SLF001

    def test_get_messages_returns_default_message(self):
        url = reverse("message-list")
        response = self.client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == [{"message": "Hello, world!"}]

    def test_get_message_detail_returns_expected_payload(self):
        url = reverse("message-detail", args=[1])
        response = self.client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == {"message": "Hello, world!"}

    def test_post_creates_new_message_and_returns_location(self):
        url = reverse("message-list")
        payload = {"message": "Hi there"}

        response = self.client.post(
            url,
            data=json.dumps(payload),
            content_type="application/json",
        )

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == {"message": "Hi there"}
        assert response["Location"].startswith("/api/v1/message/")

        detail_response = self.client.get(response["Location"])
        assert detail_response.status_code == HTTPStatus.OK
        assert detail_response.json() == {"message": "Hi there"}
