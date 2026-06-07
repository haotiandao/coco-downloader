# coding: utf-8
from typing import Any

import requests

DEFAULT_TIMEOUT = 15


class ProviderHttpClient:
    def __init__(self) -> None:
        self._session = requests.Session()

    def get_json(
        self,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
        timeout: int = DEFAULT_TIMEOUT,
        verify: bool = True,
    ) -> Any:
        response = self._session.get(
            url,
            headers=headers,
            params=params,
            timeout=timeout,
            verify=verify,
        )
        response.raise_for_status()
        return response.json()

    def get_text(
        self,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
        timeout: int = DEFAULT_TIMEOUT,
        verify: bool = True,
    ) -> str:
        response = self._session.get(
            url,
            headers=headers,
            params=params,
            timeout=timeout,
            verify=verify,
        )
        response.raise_for_status()
        return response.text

    def post_json(
        self,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        data: dict[str, Any] | None = None,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> Any:
        response = self._session.post(url, headers=headers, data=data, timeout=timeout)
        response.raise_for_status()
        return response.json()

    def post_text(
        self,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        data: dict[str, Any] | None = None,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> str:
        response = self._session.post(url, headers=headers, data=data, timeout=timeout)
        response.raise_for_status()
        return response.text

    def get_response(
        self,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> requests.Response:
        response = self._session.get(url, headers=headers, params=params, timeout=timeout)
        response.raise_for_status()
        return response

    def post_response(
        self,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        data: dict[str, Any] | None = None,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> requests.Response:
        response = self._session.post(url, headers=headers, data=data, timeout=timeout)
        response.raise_for_status()
        return response

    def head_final_url(
        self,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> str:
        response = self._session.head(
            url,
            headers=headers,
            params=params,
            timeout=timeout,
            allow_redirects=True,
        )
        response.raise_for_status()
        return response.url
