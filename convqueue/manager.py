"""Framework-agnostic batch conversion queue with cancel support."""
from __future__ import annotations

import os
import threading
from typing import Callable, Optional

from dpgcore import EncodeSettings, EncodingCancelled, EncodingError, encode, probe_duration_seconds

from convqueue.events import EventKind, ItemStatus, QueueEvent, QueueItem
from convqueue.progress import STAGE_START, STAGE_WEIGHTS, parse_ffmpeg_time

OnEvent = Callable[[QueueEvent], None]


class ConversionQueue:
    """Owns a list of QueueItems and runs them sequentially against
    dpgcore.encode() on a background thread, reporting progress via a plain
    on_event callback.

    Framework-agnostic: makes no assumption about how the caller marshals
    on_event calls onto a GUI thread. A Tk/CTk caller can drain its own
    queue.Queue on a poll loop (pass on_event=my_queue.put); a PySide6
    caller can pass a QThread's Signal.emit directly, since Qt signal
    emission across threads is already thread-safe.
    """

    def __init__(self) -> None:
        self.items: list[QueueItem] = []
        self._cancel_event = threading.Event()
        self._thread: Optional[threading.Thread] = None

    def add(self, path: str, output_path: str | None = None) -> QueueItem:
        item = QueueItem(path=path, output_path=output_path)
        self.items.append(item)
        return item

    def remove(self, item: QueueItem) -> bool:
        if item.status == ItemStatus.ENCODING:
            return False
        try:
            self.items.remove(item)
        except ValueError:
            return False
        return True

    def clear_pending(self) -> None:
        self.items = [item for item in self.items if item.status == ItemStatus.ENCODING]

    def is_running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    def start(self, settings: EncodeSettings, on_event: OnEvent) -> None:
        """Spawn a daemon thread that encodes every PENDING item in order."""
        if self.is_running():
            return
        self._cancel_event = threading.Event()
        self._thread = threading.Thread(target=self._run, args=(settings, on_event), daemon=True)
        self._thread.start()

    def cancel(self) -> None:
        """Stop the whole remaining run: the in-flight item is cancelled and
        marked CANCELLED; items not yet started stay PENDING (calling
        start() again later resumes them)."""
        self._cancel_event.set()

    def _run(self, settings: EncodeSettings, on_event: OnEvent) -> None:
        for item in self.items:
            if item.status != ItemStatus.PENDING:
                continue
            if self._cancel_event.is_set():
                break

            item.status = ItemStatus.ENCODING
            on_event(QueueEvent(kind=EventKind.STATUS, item=item))

            output_path = item.output_path or (os.path.splitext(item.path)[0] + ".dpg")

            try:
                duration = probe_duration_seconds(item.path, settings.ffprobe_path)
            except EncodingError:
                duration = 0.0

            def on_progress(stage: str, message: str, _item=item, _duration=duration) -> None:
                elapsed = parse_ffmpeg_time(message)
                if elapsed is not None and _duration > 0 and stage in STAGE_WEIGHTS:
                    fraction = STAGE_START[stage] + min(elapsed / _duration, 1.0) * STAGE_WEIGHTS[stage]
                    on_event(QueueEvent(kind=EventKind.PROGRESS, item=_item, fraction=fraction, stage=stage))
                elif stage in STAGE_START:
                    on_event(QueueEvent(kind=EventKind.PROGRESS, item=_item, fraction=STAGE_START[stage], stage=stage))
                if "time=" in message or stage in ("thumbnail", "mux", "done"):
                    on_event(QueueEvent(kind=EventKind.LOG, message=f"[{stage}] {message}"))

            try:
                encode(
                    item.path, output_path, settings,
                    on_progress=on_progress, cancel_event=self._cancel_event,
                )
                item.status = ItemStatus.DONE
                item.message = output_path
                on_event(QueueEvent(kind=EventKind.STATUS, item=item))
            except EncodingCancelled as exc:
                item.status = ItemStatus.CANCELLED
                item.message = str(exc)
                on_event(QueueEvent(kind=EventKind.STATUS, item=item))
                break
            except EncodingError as exc:
                item.status = ItemStatus.ERROR
                item.message = str(exc)
                on_event(QueueEvent(kind=EventKind.STATUS, item=item))
            except Exception as exc:  # noqa: BLE001 - surface unexpected errors, don't crash the worker thread
                item.status = ItemStatus.ERROR
                item.message = str(exc)
                on_event(QueueEvent(kind=EventKind.STATUS, item=item))

        on_event(QueueEvent(kind=EventKind.ALL_DONE))
