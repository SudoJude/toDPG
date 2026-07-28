"""Queue-level verification: batching and whole-run cancel semantics,
independent of any GUI toolkit."""
from __future__ import annotations

import time
from pathlib import Path

from convqueue import ConversionQueue, EventKind, ItemStatus
from dpgcore import EncodeSettings

ASSETS_DIR = Path(__file__).parent
SAMPLE_AVI = ASSETS_DIR / "dpg4x_example2.avi"
SAMPLE_MKV = ASSETS_DIR / "dpg4x_example1.mkv"


def test_batch_conversion_processes_all_pending_items(tmp_path: Path) -> None:
    queue = ConversionQueue()
    item1 = queue.add(str(SAMPLE_AVI), output_path=str(tmp_path / "one.dpg"))
    item2 = queue.add(str(SAMPLE_MKV), output_path=str(tmp_path / "two.dpg"))

    events = []
    queue.start(EncodeSettings(), on_event=events.append)
    while queue.is_running():
        time.sleep(0.05)

    assert item1.status == ItemStatus.DONE
    assert item2.status == ItemStatus.DONE
    assert (tmp_path / "one.dpg").exists()
    assert (tmp_path / "two.dpg").exists()
    assert any(event.kind == EventKind.ALL_DONE for event in events)


def test_cancel_stops_whole_run_leaves_remaining_pending(tmp_path: Path) -> None:
    queue = ConversionQueue()
    item1 = queue.add(str(SAMPLE_MKV), output_path=str(tmp_path / "one.dpg"))
    item2 = queue.add(str(SAMPLE_AVI), output_path=str(tmp_path / "two.dpg"))

    queue.start(EncodeSettings(), on_event=lambda _e: None)
    time.sleep(0.5)
    queue.cancel()
    while queue.is_running():
        time.sleep(0.05)

    assert item1.status == ItemStatus.CANCELLED
    assert item2.status == ItemStatus.PENDING


def test_remove_refuses_in_flight_item(tmp_path: Path) -> None:
    queue = ConversionQueue()
    item = queue.add(str(SAMPLE_MKV), output_path=str(tmp_path / "one.dpg"))

    queue.start(EncodeSettings(), on_event=lambda _e: None)
    time.sleep(0.3)
    assert item.status == ItemStatus.ENCODING
    assert queue.remove(item) is False

    queue.cancel()
    while queue.is_running():
        time.sleep(0.05)
