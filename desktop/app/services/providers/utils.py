# coding: utf-8
import base64
import json
import re
from typing import Any
from urllib.parse import quote, unquote, urljoin, urlparse


def clean_text(value: str | None) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def extract_ext(url: str, fallback: str = "mp3") -> str:
    clean_url = url.split("?", 1)[0]
    suffix = clean_url.rsplit(".", 1)
    return suffix[1] if len(suffix) > 1 and suffix[1] else fallback


def absolute_url(value: str | None, base_url: str) -> str | None:
    if not value:
        return None
    return urljoin(base_url, value)


def is_http_url(value: Any) -> bool:
    return isinstance(value, str) and value.startswith("http")


def safe_json_loads(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return {}


def decode_js_string_literal(value: str) -> str:
    escaped_value = value.replace("\"", "\\\"")
    return json.loads("\"" + escaped_value + "\"")


def quote_id(value: str) -> str:
    return quote(value, safe="")


def unquote_repeated(value: str) -> str:
    decoded = value.strip()
    for _ in range(2):
        if "%" not in decoded:
            break
        decoded = unquote(decoded)
    return decoded


def decode_base64_url(value: str, replacement: tuple[str, str] | None = None) -> str:
    source = value.replace(replacement[0], replacement[1]) if replacement else value
    try:
        padding = "=" * (-len(source) % 4)
        return base64.b64decode(source + padding).decode("utf-8")
    except (ValueError, UnicodeDecodeError):
        return ""


def strip_url_query(url: str) -> str:
    parsed = urlparse(url)
    return parsed._replace(query="", fragment="").geturl()
