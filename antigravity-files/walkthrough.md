# DPG Features: Preview, Encoder Fix, and Thumbnails

## Overview
This task encompassed three major improvements to the DPG file handling:
1.  **Verification**: Verified the "DPG Preview" feature.
2.  **Encoder Fix**: Refactored `EncoderService` to produce valid DPG files using `ffmpeg`.
3.  **Thumbnail Support**: Added thumbnail generation to created DPG files (Version 4).

## 1. DPG Preview Verification
- **Issue**: The `PreviewService` failed to generate previews because it incorrectly assumed DPG video streams were always "raw video" (RGB), failing on standard MPEG-1 streams.
- **Fix**: Updated `backend/preview_service.py` to remove restrictive flags, allowing `ffmpeg` to auto-detect the format.
- **Result**: Valid DPG files can now be previewed in the browser.

## 2. Encoder Refactor
- **Issue**: The legacy `EncoderService` produced invalid files.
- **Fix**: Rewrote `backend/encoder_service.py` to use a modern `ffmpeg` pipeline:
    - **Audio**: Encoded to MP2 (32000Hz, 128k).
    - **Video**: Encoded to MPEG-1 (256x192, 24fps).
    - **Muxing**: Implemented a custom Python muxer to build the DPG header and combine streams.

## 3. Thumbnail Support (New)
- **Feature**: Added embedded thumbnails to generated files.
- **Implementation**:
    - **Extraction**: Uses `ffmpeg` to extract a representative frame from the source video.
    - **Conversion**: Converts the frame to the specific 16-bit RGB1555 format used by DPG.
    - **Muxing**: Upgraded the output file version to **DPG4**, injecting the `THM0` marker and 96KB thumbnail data into the header.
- **Management (New)**:
    - **View**: Users can see the embedded thumbnail in the file browser.
    - **Update**: Users can upload a custom image to replace the embedded thumbnail.
- **Shared Directory (New)**:
    - **Mount**: Added `./shared` volume mount to `/app/shared`.
    - **Output**: Updated default configuration to save generated files to `/app/shared`.
- **Documentation (New)**:
    - **README.md**: Added comprehensive setup and usage guide.
    - **DPG_FORMAT.md**: Added technical specification for the DPGv4 format.
- **UI (New)**:
    - **Logo**: Added `Dpg4x_SidebarLogo.png` to the application header.
    - **Favicon**: Updated browser tab icon.
    - **Verification**:
        ![UI Logo Verification](/Users/tomasa/.gemini/antigravity/brain/a7bf2464-a386-4c24-ad1a-74a654d2bd52/verify_ui_logo_relocated_1765055202987.webp)
- **Verification**:
    - Converted `dpg4x_example2.avi`.
    - Confirmed correct DPG4 structure and thumbnail presence.
    - validated that the file works with the Info and Preview APIs.
    - Verified thumbnail update via UI.
    - Verified input/output via local `./shared` directory.

## 4. File Browser Refinements
- **Work Directory**: Implemented `/app/work` as the secure root for file operations.
- **Upload/Download**:
    - Added API endpoints for file upload and download.
    - Updated UI with "Upload File" button and download links.
- **Bug Fix**: Fixed a 500 error in `app.py` caused by a missing import of `WORK_DIR`.
- **Verification**:
    - Verified upload/download via curl and UI.
    - Confirmed file browser visibility and correct path handling.
    
    ![File Browser Verification](/Users/tomasa/.gemini/antigravity/brain/a7bf2464-a386-4c24-ad1a-74a654d2bd52/verify_upload_in_ui_1765100177518.webp)

## 5. Upload Size Increase (1GB)
- **Requirement**: Allow uploading files up to 1GB.
- **Changes**:
    - **Flask (`backend/app.py`)**: configured `MAX_CONTENT_LENGTH = 1GB`.
    - **Nginx (`frontend/nginx.conf`)**: configured `client_max_body_size 1G`.
- **Verification**:
    - Rebuilt containers.
    - Verified upload of a 50MB file (representative of large files).

## Conclusion
The system now creates fully compliant DPG4 files with thumbnails, allows them to be previewed on the web interface, supports full file management (upload/download) within a secure work directory, and handles large file uploads up to 1GB.
