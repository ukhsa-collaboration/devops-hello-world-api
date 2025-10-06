"""Gunicorn entry point that mirrors the shell-based runner."""

from __future__ import annotations

import os
from typing import Any

import gunicorn.app.base
from django.core.management import call_command

from hello_world_api.wsgi import application


class Application(gunicorn.app.base.BaseApplication):
    def __init__(self, app: Any, options: dict[str, Any] | None = None) -> None:
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self) -> None:
        valid_settings = self.cfg.settings
        config = {
            key: value
            for key, value in self.options.items()
            if key in valid_settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self) -> Any:
        return self.application


if __name__ == "__main__":
    host = os.environ.get("GUNICORN_HOST", "0.0.0.0")  # noqa: S104
    port = os.environ.get("GUNICORN_PORT", "8000")
    workers = int(os.environ.get("GUNICORN_WORKERS", "2"))
    migrate_enabled = bool(os.environ.get("DJANGO_MIGRATE", True))  # noqa: PLW1508
    collectstatic_enabled = bool(os.environ.get("DJANGO_COLLECTSTATIC", False))  # noqa: PLW1508
    dev_server_enabled = bool(os.environ.get("DJANGO_DEV_SERVER", False))  # noqa: PLW1508

    if not dev_server_enabled:
        call_command("check", deploy=True)

    if migrate_enabled:
        call_command("migrate", interactive=False)

    if collectstatic_enabled:
        call_command("collectstatic", interactive=False, verbosity=0)
    else:
        pass

    if dev_server_enabled:
        call_command("runserver", f"{host}:{port}")
    else:
        options = {
            "bind": f"{host}:{port}",
            "workers": workers,
            "access-logfile": "-",
            "error-logfile": "-",
        }
        Application(application, options).run()
