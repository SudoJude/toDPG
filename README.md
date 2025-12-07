# DPG4x-Web

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
