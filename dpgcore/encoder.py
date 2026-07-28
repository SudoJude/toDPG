"""
Core DPG encoding pipeline: audio/video transcoding via FFmpeg, thumbnail
extraction, and DPG container muxing.

This module is intentionally free of any web/UI framework dependency
(no Flask, no Docker, no threading-based job state). It exposes a single
synchronous `encode()` function that a caller — a CLI, a desktop UI, or a
web route — can run directly or on a thread/process of its own choosing,
optionally receiving progress updates via a callback and cancelling via a
threading.Event.
"""
from __future__ import annotations

import os
import shutil
import struct
import subprocess
import tempfile
import threading
from dataclasses import dataclass
from typing import Callable, Optional

from dpgcore.constants import AUDIO_CHANNELS, snap_audio_frequency, snap_fps
from dpgcore.dpg_header import (
    DpgHeader,
    PIXEL_FORMAT_RGB24,
    THUMBNAIL_HEIGHT,
    THUMBNAIL_SIZE_BYTES,
    THUMBNAIL_WIDTH,
)
from dpgcore.exceptions import (
    EncodingCancelled,
    EncodingError,
    FFmpegNotFoundError,
    ProbeError,
    SubprocessFailedError,
)

ProgressCallback = Callable[[str, str], None]  # (stage, message) -> None

# How often the cancel-watcher thread polls the cancel event, in seconds.
_CANCEL_POLL_INTERVAL = 0.2
# How long to wait for a terminated process to exit before SIGKILL-ing it.
_TERMINATE_GRACE_SECONDS = 3
# ffprobe should return almost instantly; this is a hang backstop, not a
# realistic budget.
_PROBE_TIMEOUT_SECONDS = 30


@dataclass
class EncodeSettings:
    dpg_version: int = 4
    video_fps: float = 24.0
    video_bitrate_kbps: int = 256
    video_width: int = THUMBNAIL_WIDTH
    video_height: int = THUMBNAIL_HEIGHT
    audio_codec: str = "mp2"
    audio_bitrate_kbps: int = 128
    audio_frequency: int = 32000
    audio_channels: int = 2
    ffmpeg_path: str = "ffmpeg"
    ffprobe_path: str = "ffprobe"

    def __post_init__(self) -> None:
        # Snap to MPEG-1/DPG-safe values so arbitrary GUI- or file-derived
        # settings can never reach ffmpeg's argv and crash the encoder.
        self.video_fps = snap_fps(self.video_fps)
        self.audio_frequency = snap_audio_frequency(self.audio_frequency)
        self.audio_channels = AUDIO_CHANNELS


@dataclass
class EncodeResult:
    output_path: str
    frames: int
    duration_seconds: float
    video_size_bytes: int
    audio_size_bytes: int


def _report(on_progress: Optional[ProgressCallback], stage: str, message: str) -> None:
    if on_progress:
        on_progress(stage, message)


def _watch_for_cancel(process: subprocess.Popen, cancel_event: threading.Event) -> None:
    """Terminate `process` if `cancel_event` is set while it's still running.

    Runs on its own daemon thread so it can act even if the caller's thread
    is blocked reading the process's stdout (e.g. a hung/silent ffmpeg).
    Exits on its own once the process finishes, so it never outlives the
    _run() call that started it.
    """
    while process.poll() is None:
        if cancel_event.wait(timeout=_CANCEL_POLL_INTERVAL):
            process.terminate()
            try:
                process.wait(timeout=_TERMINATE_GRACE_SECONDS)
            except subprocess.TimeoutExpired:
                process.kill()
            return


def _run(
    cmd: list[str],
    stage: str,
    on_progress: Optional[ProgressCallback],
    cancel_event: Optional[threading.Event] = None,
) -> None:
    """Run a subprocess, streaming stderr/stdout lines to on_progress."""
    _report(on_progress, stage, f"$ {' '.join(cmd)}")
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        )
    except OSError as exc:
        raise FFmpegNotFoundError(f"Could not run {cmd[0]!r}: {exc}") from exc

    watcher: Optional[threading.Thread] = None
    if cancel_event is not None:
        watcher = threading.Thread(
            target=_watch_for_cancel, args=(process, cancel_event), daemon=True
        )
        watcher.start()

    for line in process.stdout:
        line = line.strip()
        if line:
            _report(on_progress, stage, line)
    return_code = process.wait()

    if cancel_event is not None and cancel_event.is_set():
        raise EncodingCancelled(f"{stage} cancelled")
    if return_code != 0:
        raise SubprocessFailedError(stage, return_code, cmd)


def probe_duration_seconds(media_path: str, ffprobe_path: str = "ffprobe") -> float:
    """Return a media file's duration in seconds via ffprobe. Public so
    callers (e.g. a GUI) can estimate progress before/independent of encode()."""
    cmd = [
        ffprobe_path,
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        media_path,
    ]
    try:
        output = subprocess.check_output(
            cmd, universal_newlines=True, timeout=_PROBE_TIMEOUT_SECONDS
        ).strip()
        return float(output)
    except FileNotFoundError as exc:
        raise FFmpegNotFoundError(f"Could not run {ffprobe_path!r}: {exc}") from exc
    except subprocess.TimeoutExpired as exc:
        raise ProbeError(f"Timed out determining duration of {media_path}") from exc
    except (subprocess.CalledProcessError, ValueError) as exc:
        raise ProbeError(f"Could not determine duration of {media_path}: {exc}") from exc


def rgb24_to_rgb1555(raw_rgb24: bytes) -> bytes:
    """Pack RGB24 pixel data into DPG's 16-bit A1 R5 G5 B5 format."""
    if len(raw_rgb24) % 3 != 0:
        raise ValueError("RGB24 buffer length must be a multiple of 3")
    packed = bytearray(len(raw_rgb24) // 3 * 2)
    for i in range(0, len(raw_rgb24), 3):
        r, g, b = raw_rgb24[i], raw_rgb24[i + 1], raw_rgb24[i + 2]
        pixel = (1 << 15) | ((b >> 3) << 10) | ((g >> 3) << 5) | (r >> 3)
        struct.pack_into("<H", packed, (i // 3) * 2, pixel)
    return bytes(packed)


def _extract_thumbnail(
    input_path: str,
    ffmpeg_path: str,
    on_progress: Optional[ProgressCallback],
    work_dir: str,
    cancel_event: Optional[threading.Event] = None,
) -> bytes:
    thumb_raw_path = os.path.join(work_dir, "thumb.raw")
    cmd = [
        ffmpeg_path, "-y",
        "-i", input_path,
        "-vf", f"thumbnail,scale={THUMBNAIL_WIDTH}:{THUMBNAIL_HEIGHT}",
        "-frames:v", "1",
        "-f", "rawvideo",
        "-pix_fmt", "rgb24",
        "--", thumb_raw_path,
    ]
    try:
        _run(cmd, "thumbnail", on_progress, cancel_event=cancel_event)
    except EncodingCancelled:
        raise
    except EncodingError:
        pass  # fall through to blank-thumbnail handling below

    if os.path.exists(thumb_raw_path):
        with open(thumb_raw_path, "rb") as f:
            raw_rgb24 = f.read()
        if len(raw_rgb24) == THUMBNAIL_WIDTH * THUMBNAIL_HEIGHT * 3:
            return rgb24_to_rgb1555(raw_rgb24)
        _report(on_progress, "thumbnail", "extracted frame had unexpected size, using blank thumbnail")
    else:
        _report(on_progress, "thumbnail", "extraction failed, using blank thumbnail")

    return b"\x00" * THUMBNAIL_SIZE_BYTES


def _check_cancelled(cancel_event: Optional[threading.Event], stage: str) -> None:
    if cancel_event is not None and cancel_event.is_set():
        raise EncodingCancelled(f"{stage} cancelled before starting")


def encode(
    input_path: str,
    output_path: str,
    settings: Optional[EncodeSettings] = None,
    on_progress: Optional[ProgressCallback] = None,
    cancel_event: Optional[threading.Event] = None,
) -> EncodeResult:
    """
    Transcode `input_path` (any FFmpeg-readable media file) into a DPG file
    at `output_path`, using `settings` for video/audio/DPG parameters.

    Raises EncodingError (or a subclass) on any FFmpeg or muxing failure,
    and EncodingCancelled if `cancel_event` is set while encoding is in
    progress. Does not validate that `input_path`/`output_path` are within
    any particular directory — that is the caller's concern (a web route, a
    file-picker dialog, etc.).
    """
    settings = settings or EncodeSettings()

    if not os.path.isfile(input_path):
        raise EncodingError(f"Input file not found: {input_path}")

    with tempfile.TemporaryDirectory(prefix="dpgcore_") as work_dir:
        audio_temp = os.path.join(work_dir, "audio.mp2")
        video_temp = os.path.join(work_dir, "video.m1v")

        _check_cancelled(cancel_event, "audio")
        _report(on_progress, "audio", "encoding audio stream")
        audio_cmd = [
            settings.ffmpeg_path, "-y",
            "-i", input_path,
            "-vn",
            "-c:a", settings.audio_codec,
            "-ar", str(settings.audio_frequency),
            "-ac", str(settings.audio_channels),
            "-b:a", f"{settings.audio_bitrate_kbps}k",
            "-f", "mp2",
            "--", audio_temp,
        ]
        _run(audio_cmd, "audio", on_progress, cancel_event=cancel_event)

        _check_cancelled(cancel_event, "video")
        _report(on_progress, "video", "encoding video stream")
        video_cmd = [
            settings.ffmpeg_path, "-y",
            "-i", input_path,
            "-an",
            "-c:v", "mpeg1video",
            "-s", f"{settings.video_width}x{settings.video_height}",
            "-r", str(settings.video_fps),
            "-b:v", f"{settings.video_bitrate_kbps}k",
            "-f", "mpeg1video",
            "--", video_temp,
        ]
        _run(video_cmd, "video", on_progress, cancel_event=cancel_event)

        _check_cancelled(cancel_event, "thumbnail")
        _report(on_progress, "thumbnail", "extracting thumbnail")
        thumb_data = _extract_thumbnail(
            input_path, settings.ffmpeg_path, on_progress, work_dir, cancel_event=cancel_event
        )

        # Probe the *source* file's duration, not the raw .m1v elementary
        # stream: a headerless MPEG-1 video stream has no reliable container
        # duration for ffprobe to read.
        duration_seconds = probe_duration_seconds(input_path, settings.ffprobe_path)
        frames = round(duration_seconds * settings.video_fps)

        audio_size = os.path.getsize(audio_temp)
        video_size = os.path.getsize(video_temp)

        _report(on_progress, "mux", "writing DPG header and streams")
        header = DpgHeader()
        header.setVideo(frames=frames, fps=round(settings.video_fps), pixel=PIXEL_FORMAT_RGB24)
        header.setAudio(codec=settings.audio_codec, sampleRate=settings.audio_frequency)
        header.setSizes(version=settings.dpg_version, vSize=video_size, aSize=audio_size, gSize=0)

        header_temp = os.path.join(work_dir, "header.bin")
        header.toFile(header_temp)

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "wb") as out_f:
            with open(header_temp, "rb") as hf:
                shutil.copyfileobj(hf, out_f)
            if settings.dpg_version >= 4:
                out_f.write(thumb_data)
            with open(audio_temp, "rb") as af:
                shutil.copyfileobj(af, out_f)
            with open(video_temp, "rb") as vf:
                shutil.copyfileobj(vf, out_f)

        _report(on_progress, "done", f"wrote {output_path}")

        return EncodeResult(
            output_path=output_path,
            frames=frames,
            duration_seconds=duration_seconds,
            video_size_bytes=video_size,
            audio_size_bytes=audio_size,
        )
