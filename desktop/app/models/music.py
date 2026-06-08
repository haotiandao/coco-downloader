# coding: utf-8
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class MusicItem:
    id: str
    title: str
    artist: str
    provider: str
    album: str | None = None
    cover: str | None = None
    duration: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PlayInfo:
    url: str
    type: str
    bitrate: str | None = None
    cover: str | None = None
    headers: dict[str, str] = field(default_factory=dict)
