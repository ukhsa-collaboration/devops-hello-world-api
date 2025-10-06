"""View functions for the hello world API endpoints."""

import json

from django.http import Http404
from django.http import HttpResponseNotAllowed
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

_MESSAGES = {1: "Hello, world!"}
_NEXT_MESSAGE_ID = 2


def _messages_payload():
    return [{"message": text} for text in _MESSAGES.values()]


@csrf_exempt
def messages(request):
    if request.method == "GET":
        return JsonResponse(_messages_payload(), safe=False)

    if request.method == "POST":
        try:
            payload = json.loads(request.body or b"{}")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON body."}, status=400)

        message_text = payload.get("message")
        if not isinstance(message_text, str) or not message_text.strip():
            return JsonResponse(
                {"error": "`message` must be a non-empty string."},
                status=400,
            )

        message_text = message_text.strip()

        global _NEXT_MESSAGE_ID  # noqa: PLW0603
        message_id = _NEXT_MESSAGE_ID
        _NEXT_MESSAGE_ID += 1
        _MESSAGES[message_id] = message_text

        response = JsonResponse({"message": message_text}, status=201)
        response["Location"] = f"/v1/message/{message_id}"
        return response

    return HttpResponseNotAllowed(["GET", "POST"])


def message_detail(request, message_id):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    try:
        message_text = _MESSAGES[message_id]
    except KeyError as exc:  # pragma: no cover - defensive programming
        msg = "Message not found."
        raise Http404(msg) from exc

    return JsonResponse({"message": message_text})
