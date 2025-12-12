# DPG4x-Web

dpg4x - ongoing web migration for the project https://sourceforge.net/p/dpg4x/master/ci/migration_web/tree/

[![CI](https://github.com/d0malaga/dpg4x/actions/workflows/ci-docker-compose.yml/badge.svg?branch=migration_web)](https://github.com/d0malaga/dpg4x/actions/workflows/ci-docker-compose.yml)

A modern web-based converter and manager for DPG video files (used by Nintendo DS homebrew players like Moonshell).

## Features

- **Convert Video**: Transcode AVI/MP4/MKV to DPG (Version 4).
- **Correctness**: Generates fully compliant DPG4 files with proper headers and audio/video sync.
- **Thumbnails**: Automatically extracts and embeds thumbnails. Supports updating thumbnails via the UI.
- **Preview**: Watch generated DPG files directly in the browser.
- **Manage Files**: Browse, manage, and download files via a web interface.
- **Shared Directory**: Mounts a local `./shared` directory for easy drag-and-drop input/output.

## Setup

### Prerequisites
- Docker and Docker Compose

### Running the Application

1.  **Start the services**:
    ```bash
    docker-compose up -d
    ```

2.  **Access the Web UI**:
    Open [http://localhost:8080](http://localhost:8080) in your browser.

3.  **Shared Folder**:
    Place video files you want to convert into the `shared` folder in this directory.
    Converted files will also appear in the `shared` folder.

## Usage

1.  **Convert a File**:
    - Browse to your file in the web UI.
    - Click "Convert".
    - The conversion status will appear.
    
2.  **View/Change Thumbnail**:
    - Click on a `.dpg` file.
    - The current thumbnail is displayed in the info panel.
    - Click "Choose File" under "Change Thumbnail" to upload a new image (JPG/PNG).
    - Click "Update" to apply.

3.  **Preview**:
    - Click on a `.dpg` file.
    - Click "Preview Video" to watch it in the browser.

## Development

- **Backend**: Python Flask (Port 5001)
- **Frontend**: Angular (Port 8080)

To rebuild after changes:
```bash
docker-compose up -d --build
```

## Continuous Integration (CI)

This repository includes a GitHub Actions workflow that builds and exercises the services using `docker compose`.

- Workflow path: `.github/workflows/ci-docker-compose.yml`
- Runner: `ubuntu-latest` (uses the Compose V2 CLI via `docker compose`)

How the CI job works (summary):

- Checks out the repo.
- Sets up QEMU and Buildx (useful for multi-arch builds).
- Runs `docker compose -f docker-compose.yml up --build -d` to build and start services.
- Shows running services with `docker compose ps`.
- Tears down the compose stack with `docker compose down --volumes --remove-orphans`.

Run locally (same commands CI uses):

```bash
# build and start services in background
# optionally copy .env.example to .env to override host port mappings
# e.g. set BACKEND_HOST_PORT and FRONTEND_HOST_PORT
cp .env.example .env 2>/dev/null || true
docker compose -f docker-compose.yml up --build -d

# show running services
docker compose -f docker-compose.yml ps

# run a command inside a service (example: run backend tests)
docker compose exec -T backend python -m pytest

# stop and remove services, volumes
docker compose -f docker-compose.yml down --volumes --remove-orphans
```

Notes and customization:

- If your environment does not have the Compose V2 plugin, use the `docker/compose-action@v2` GitHub Action or install the `docker-compose` binary.
- For GitLab CI or other CI providers that use Docker-in-Docker (DinD), you may need a `privileged` runner or use the Docker socket bind approach on self-hosted runners.
- Adjust the service name (`backend` in the example) and test commands to match your test setup.

If you want, I can add a short `README` badge or expand the workflow to run your tests automatically — tell me which service(s) and test commands to run in CI.
