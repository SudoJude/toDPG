"""Typed events for ConversionQueue — no GUI-toolkit dependency."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ItemStatus(Enum):
    PENDING = "Pending"
    ENCODING = "Encoding"
    DONE = "Done"
    ERROR = "Error"
    CANCELLED = "Cancelled"


@dataclass
class QueueItem:
    path: str
    output_path: str | None = None
    status: ItemStatus = ItemStatus.PENDING
    message: str = ""


class EventKind(Enum):
    STATUS = "status"
    PROGRESS = "progress"
    LOG = "log"
    ALL_DONE = "all_done"


@dataclass
class QueueEvent:
    kind: EventKind
    item: QueueItem | None = None
    fraction: float | None = None  # 0.0-1.0, PROGRESS only
    stage: str | None = None
    message: str = ""
