"""Progress-fraction estimation from ffmpeg's stderr `time=` output."""
from __future__ import annotations

import re

# Fraction of overall progress attributed to each encode() stage.
STAGE_WEIGHTS = {"audio": 0.15, "video": 0.80, "thumbnail": 0.03, "mux": 0.02, "done": 0.0}
STAGE_START = {"audio": 0.0, "video": 0.15, "thumbnail": 0.95, "mux": 0.98, "done": 1.0}

_TIME_RE = re.compile(r"time=(\d+):(\d+):(\d+\.?\d*)")


def parse_ffmpeg_time(line: str) -> float | None:
    match = _TIME_RE.search(line)
    if not match:
        return None
    hours, minutes, seconds = match.groups()
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)
