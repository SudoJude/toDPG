"""
MPEG-1/DPG-safe encoding constants and value-snapping helpers.

ffmpeg's mpeg1video encoder only accepts standard MPEG-1 frame rates, and DPG
audio is always stereo at one of a small set of sample rates. These functions
snap arbitrary caller-supplied values to the nearest valid one rather than
raising, so a bad fps/sample rate from a GUI or a probed source file can
never reach ffmpeg's argv and crash the encoder.
"""
from __future__ import annotations

VALID_FPS: tuple[float, ...] = (23.976, 24.0, 25.0, 29.97, 30.0)
VALID_AUDIO_FREQUENCIES: tuple[int, ...] = (32000, 44100)
AUDIO_CHANNELS = 2  # DPG audio is always stereo


def snap_fps(fps: float) -> float:
    """Return the VALID_FPS value nearest to `fps`."""
    return min(VALID_FPS, key=lambda v: abs(v - fps))


def snap_audio_frequency(freq: int) -> int:
    """Return the VALID_AUDIO_FREQUENCIES value nearest to `freq`."""
    return min(VALID_AUDIO_FREQUENCIES, key=lambda v: abs(v - freq))
