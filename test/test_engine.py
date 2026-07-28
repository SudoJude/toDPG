"""End-to-end verification of dpgcore's validation, error handling, and
cancellation, using the real sample videos checked into test/."""
from __future__ import annotations

import threading
import time
from pathlib import Path

import pytest

from dpgcore import EncodeSettings, encode, probe_duration_seconds
from dpgcore.exceptions import (
    EncodingCancelled,
    EncodingError,
    FFmpegNotFoundError,
    SubprocessFailedError,
)

ASSETS_DIR = Path(__file__).parent
SAMPLE_AVI = ASSETS_DIR / "dpg4x_example2.avi"
SAMPLE_MKV = ASSETS_DIR / "dpg4x_example1.mkv"


@pytest.fixture
def corrupt_video(tmp_path: Path) -> Path:
    """A truncated, unreadable-as-video file built from a real sample's header."""
    corrupt = tmp_path / "corrupt.avi"
    with open(SAMPLE_AVI, "rb") as src:
        corrupt.write_bytes(src.read(4096))
    return corrupt


def test_golden_path_produces_valid_dpg(tmp_path: Path) -> None:
    output = tmp_path / "out.dpg"
    result = encode(str(SAMPLE_AVI), str(output), EncodeSettings())
    assert output.exists()
    assert output.stat().st_size > 0
    assert result.output_path == str(output)
    assert result.frames > 0


def test_fps_snaps_to_nearest_valid_mpeg1_rate() -> None:
    assert EncodeSettings(video_fps=27).video_fps == 25.0
    assert EncodeSettings(video_fps=23.976).video_fps == 23.976
    assert EncodeSettings(video_fps=100).video_fps == 30.0


def test_audio_snaps_to_stereo_and_valid_frequency() -> None:
    settings = EncodeSettings(audio_frequency=48000, audio_channels=1)
    assert settings.audio_frequency == 44100
    assert settings.audio_channels == 2


def test_missing_ffmpeg_binary_raises_specific_error(tmp_path: Path) -> None:
    settings = EncodeSettings(ffmpeg_path="/nonexistent/ffmpeg-xyz")
    with pytest.raises(FFmpegNotFoundError):
        encode(str(SAMPLE_AVI), str(tmp_path / "out.dpg"), settings)


def test_missing_ffprobe_binary_raises_specific_error() -> None:
    with pytest.raises(FFmpegNotFoundError):
        probe_duration_seconds(str(SAMPLE_AVI), ffprobe_path="/nonexistent/ffprobe-xyz")


def test_corrupt_input_raises_encoding_error_not_crash(corrupt_video: Path, tmp_path: Path) -> None:
    with pytest.raises(SubprocessFailedError):
        encode(str(corrupt_video), str(tmp_path / "out.dpg"), EncodeSettings())


def test_cancellation_stops_ffmpeg_and_cleans_temp_dir(tmp_path: Path) -> None:
    cancel_event = threading.Event()
    result: dict = {}

    def run() -> None:
        try:
            encode(
                str(SAMPLE_MKV), str(tmp_path / "out.dpg"), EncodeSettings(),
                cancel_event=cancel_event,
            )
        except Exception as exc:  # noqa: BLE001 - captured for the assertion below
            result["exc"] = exc

    before = set(Path(tempfile_root()).glob("dpgcore_*"))
    thread = threading.Thread(target=run)
    thread.start()
    time.sleep(0.5)
    cancel_event.set()
    thread.join(timeout=10)

    assert not thread.is_alive()
    assert isinstance(result.get("exc"), EncodingCancelled)
    after = set(Path(tempfile_root()).glob("dpgcore_*"))
    assert after - before == set()


def tempfile_root() -> str:
    import tempfile

    return tempfile.gettempdir()
