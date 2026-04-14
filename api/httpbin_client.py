import json
from typing import Any

import allure
from requests import Response, Session


class HttpBinClient:
    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = Session()
        self.session.headers.update({"User-Agent": "qa-framework/1.0"})

    def _build_url(self, path: str) -> str:
        if not path.startswith("/"):
            path = f"/{path}"
        return f"{self.base_url}{path}"

    def request(self, method: str, path: str, **kwargs: Any) -> Response:
        kwargs.pop("expected_status", None)
        timeout = kwargs.pop("timeout", self.timeout)
        url = self._build_url(path)

        response = self.session.request(
            method=method, url=url, timeout=timeout, **kwargs
        )
        self._attach_request_response(method, url, kwargs, response)

        return response

    def get(self, path: str, **kwargs: Any) -> Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> Response:
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs: Any) -> Response:
        return self.request("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs: Any) -> Response:
        return self.request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> Response:
        return self.request("DELETE", path, **kwargs)

    @staticmethod
    def _attach_request_response(
        method: str, url: str, request_kwargs: dict[str, Any], response: Response
    ) -> None:
        allure.attach(
            f"{method} {url}",
            name="request_line",
            attachment_type=allure.attachment_type.TEXT,
        )

        if request_kwargs.get("params"):
            allure.attach(
                json.dumps(request_kwargs["params"], ensure_ascii=False, indent=2),
                name="request_params",
                attachment_type=allure.attachment_type.JSON,
            )

        if request_kwargs.get("headers"):
            allure.attach(
                json.dumps(request_kwargs["headers"], ensure_ascii=False, indent=2),
                name="request_headers",
                attachment_type=allure.attachment_type.JSON,
            )

        if request_kwargs.get("json") is not None:
            allure.attach(
                json.dumps(request_kwargs["json"], ensure_ascii=False, indent=2),
                name="request_json",
                attachment_type=allure.attachment_type.JSON,
            )

        allure.attach(
            str(response.status_code),
            name="response_status",
            attachment_type=allure.attachment_type.TEXT,
        )

        allure.attach(
            response.text,
            name="response_body",
            attachment_type=allure.attachment_type.TEXT,
        )
