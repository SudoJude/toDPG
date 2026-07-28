"""Exception hierarchy for dpgcore encoding failures."""
from __future__ import annotations


class EncodingError(Exception):
    """Base class for all dpgcore encoding failures."""


class FFmpegNotFoundError(EncodingError):
    """ffmpeg/ffprobe binary missing or not executable."""


class SubprocessFailedError(EncodingError):
    """ffmpeg/ffprobe exited non-zero."""

    def __init__(self, stage: str, returncode: int, cmd: list[str]):
        self.stage = stage
        self.returncode = returncode
        self.cmd = cmd
        super().__init__(f"{stage} failed (exit code {returncode})")


class ProbeError(EncodingError):
    """ffprobe ran but produced unusable output (corrupt file, bad duration, timeout)."""


class EncodingCancelled(EncodingError):
    """Raised when a caller-supplied cancel_event was set mid-encode."""
