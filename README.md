# toDPG

A converter/manager for **DPG video files** — the format used by Nintendo DS homebrew media players like Moonshell. toDPG is a fork of [dpg4x](https://sourceforge.net/p/dpg4x/master/ci/migration_web/tree/).

See [DPG_FORMAT.md](DPG_FORMAT.md) for the binary format spec.

## Project status

toDPG is migrating from a Docker Compose web app (Flask + Angular) to a **standalone Python desktop application** (CustomTkinter). This migration is in progress.

- `dpgcore/` — framework-free DPG encoding library (FFmpeg transcoding, header read/write, thumbnail packing). This is the actively developed core logic.
- `desktop/` — CustomTkinter desktop GUI built on `dpgcore`.
- `backend/` / `frontend/` — the legacy Flask/Angular web app. Still functional, no longer the focus of new work.
- `org_dpg4x/` — original upstream dpg4x source, kept for reference.

## Running the desktop app

### Prerequisites
- Python 3.11+
- FFmpeg and ffprobe on your `PATH`

### Setup

```bash
pip install -r desktop/requirements.txt
python -m desktop
```

Drag and drop video files (AVI/MP4/MKV/etc.) into the window, adjust resolution/FPS, and convert to `.dpg`.

## Running the legacy web app

The Docker-based web app still works if you need it:

```bash
docker-compose up -d
```

Then open [http://localhost:8080](http://localhost:8080). See `docker-compose.yml` for details.

## Contributing

This project is under active migration — expect things to move around.

## AI Disclaimer

The original app this project was based upon frequently used AI coding agents to help with development. As much of this project was already written with AI by the original developer, I have also used Claude Code in certain areas to help with development. No code is published without being thoroughly reviewed, and I have the same high code quality standards for toDPG as my other projects.

## License

toDPG is licensed under the [GNU General Public License v3.0](LICENSE), the same license as upstream dpg4x.
