from typing import Any
import logging
import urllib.parse
import requests
from pylib_0xe.database.mediators.engine_mediator import singleton
from pylib_0xe.config.config import Config

from src.types.api.server_response import ServerResponse

LOGGER = logging.getLogger(__name__)


@singleton
class BackboneServer:
    password: str
    username: str
    base_url: str
    token: str

    def __init__(self) -> None:
        self.password = Config.read_env("backbone_server.credentials.password")
        self.username = Config.read_env("backbone_server.credentials.username")
        self.base_url = Config.read_env("backbone_server.base_url")

    def send_mail(self, email: str, title: str, body: str) -> ServerResponse:
        if not self._ping():
            self._login()
        email = self._uri_encode(email)
        title = self._uri_encode(title)
        response = self._request(
            "/mail/send-mail", email=email, title=title, request_body=body
        )
        return ServerResponse(status=response.status_code, message=response.text)

    def _ping(self) -> bool:
        """Checks whether the credentials have more remaining time"""
        try:
            response = self._request("/utils/ping")
            response.raise_for_status()
            if response.json().remaining_time > Config.read(
                "api.ping.acceptable_remaining_time"
            ):
                return True
        except Exception:
            pass
        return False

    def _login(self) -> ServerResponse:
        LOGGER.info("in the login request")
        self.token = ""
        response = self._request(
            "/auth/login", username=self.username, password=self.password
        )
        response.raise_for_status()
        self.token = response.json().strip()
        LOGGER.info(f"token is {self.token}")
        return ServerResponse(status=response.status_code, message=response.text)

    def _uri_encode(self, value: Any) -> str:
        return urllib.parse.quote(value)

    def _request(
        self, endpoint: str, method: str = "POST", request_body: str = "", **kwargs
    ) -> requests.Response:
        # Create base URL
        url = self.base_url.strip()
        if url[-1] == "/":
            url = url[:-1]
        url += endpoint

        # Add key-values
        first = True
        for key, value in kwargs.items():
            if first:
                url += "?"
                first = False
            else:
                url += "&"
            url += f"{key}={value}"

        # Set authentication header
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        # Send request
        if method == "POST":
            return requests.post(url, headers=headers, json=request_body)
        elif method == "GET":
            return requests.get(url, headers=headers)
        else:
            raise Exception("Invalid request method")
