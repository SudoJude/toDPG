# Implementation Plan - dpg4x Rewrite (Angular + Flask)

The goal is to rewrite the existing wxPython `dpg4x` application into a modern web application using Angular for the frontend and Python Flask for the backend. The application converts video files to DPG format for Nintendo DS.

## User Review Required

> [!IMPORTANT]
> **File Access Strategy**: The original app is a desktop app that processes local files. The new web app will run locally. To avoid uploading large video files to the "server" (which is just localhost), the backend will provide a **File Browser API** to select files directly from the host filesystem. This mimics the desktop experience.

> [!WARNING]
> **Dependencies**: The backend requires `mplayer` and `mencoder` to be installed on the system, just like the original app.

## Proposed Changes

### Directory Structure
The project will be reorganized:
- `backend/`: Flask application (API + Core Logic)
- `frontend/`: Angular application
- `dpg4x/`: Legacy code (reference)

### Backend (Flask)
The backend will expose a REST API and handle the heavy lifting (encoding).

#### [NEW] [backend/app.py](file:///Users/tomasa/src/own/dpg4x-master/backend/app.py)
- Entry point for the Flask application.
- Routes:
    - `GET /api/files?path=...`: List files in a directory (for file selection).
    - `GET /api/config`: Get current configuration.
    - `POST /api/config`: Update configuration.
    - `POST /api/convert`: Start conversion process.
    - `GET /api/status`: Get current conversion status/progress.
    - `POST /api/cancel`: Cancel current conversion.

#### [NEW] [backend/encoder_service.py](file:///Users/tomasa/src/own/dpg4x-master/backend/encoder_service.py)
- Ported logic from `dpg4x/Encoder.py`.
- Class `EncoderService` to manage the `mencoder`/`mplayer` subprocesses.
- Handles threading and progress tracking.

#### [NEW] [backend/config_manager.py](file:///Users/tomasa/src/own/dpg4x-master/backend/config_manager.py)
- Ported logic from `dpg4x/ConfigurationManager.py`.
- Manages reading/writing settings (likely to a JSON file or keeping INI for compatibility).

#### [NEW] [backend/globals.py](file:///Users/tomasa/src/own/dpg4x-master/backend/globals.py)
- simplified globals for the flask app.

### Frontend (Angular)
The frontend will provide the UI.

#### [NEW] `frontend/` (Angular CLI Project)
- **Components**:
    - `FileBrowserComponent`: Navigate and select files from the server.
    - `SettingsComponent`: Configure Video, Audio, and Subtitle settings.
    - `DashboardComponent`: Main view combining file list and controls.
    - `ProgressComponent`: Show conversion progress.
- **Services**:
    - `ApiService`: Communicate with Flask backend.

## Verification Plan

### Automated Tests
- **Backend Tests**:
    - Unit tests for `config_manager.py` (read/write settings).
    - Mock tests for `encoder_service.py` (verify `subprocess` calls are constructed correctly without actually running `mencoder`).
    - API tests using `pytest` and `flask.testing`.

### Manual Verification
1.  **Setup**:
    - Start Flask backend: `python backend/app.py`
    - Start Angular frontend: `ng serve`
2.  **File Selection**:
    - Open web app.
    - Navigate directories using the File Browser.
    - Select a video file.
3.  **Configuration**:
    - Change video bitrate and audio settings.
    - Save settings (verify persistence).
4.  **Conversion**:
    - Click "Convert".
    - Verify progress bar updates.
    - Verify `mencoder` process is running on the system.
    - Verify output file is created and playable (if `mplayer` is available).
