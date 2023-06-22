# RASCUNHO

from __future__ import annotations
from typing import Callable,TypeAlias
from dataclasses import dataclass

UserId: TypeAlias = str
Topic: TypeAlias = str


@dataclass(frozen=True, kw_only=True, slots=True)
class Content:
    author: UserId
    topic: Topic
    data: str

FnNotify: TypeAlias = Callable[[list[Content]], None]
