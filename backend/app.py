import os
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename, safe_join

# Project imports
from config_manager import ConfigManager
from encoder_service import EncoderService
from preview_service import PreviewService
from thumbnail_service import ThumbnailService
from dpg_header import DpgHeader
from globals import WORK_DIR, TEMP_DIR

app = Flask(__name__)

def _resolve_and_validate(path):
    """
    Normalize the provided path and ensure it resides inside WORK_DIR.
    Uses safe_join for security and absolute path comparison for validation.
    """
    if not path:
        return None

    # Use safe_join to handle relative paths securely
    # It prevents ".." from escaping the base directory
    work_dir_abs = os.path.abspath(WORK_DIR)

    # Remove WORK_DIR from path to make it relative to WORK_DIR
    # and be able to use safe_join
    safe_path = safe_join(WORK_DIR, path.replace(work_dir_abs + os.sep, ""))
        
    if not safe_path:
        return None

    # Normalize and get absolute paths for strict comparison
    p = os.path.abspath(safe_path)

    # Final check: the resolved path MUST be within WORK_DIR
    if p == work_dir_abs or p.startswith(work_dir_abs + os.sep):
        return p
    return None

config_manager = ConfigManager()
encoder_service = EncoderService(config_manager)
preview_service = PreviewService(TEMP_DIR)
thumbnail_service = ThumbnailService(config_manager)

@app.route('/api/files', methods=['GET'])
def list_files():
    path = request.args.get('path', WORK_DIR)

    # Normalize and validate the path; fall back to WORK_DIR on invalid input
    resolved = _resolve_and_validate(path)
    if resolved is None:
        resolved = WORK_DIR

    if not os.path.exists(resolved):
        return jsonify({"error": "Path does not exist"}), 404

    # Ensure WORK_DIR exists
    if not os.path.exists(WORK_DIR):
        os.makedirs(WORK_DIR)
    
    try:
        items = []
        for entry in os.scandir(resolved):
            items.append({
                "name": entry.name,
                "path": entry.path,
                "is_dir": entry.is_dir(),
                "size": entry.stat().st_size if not entry.is_dir() else 0
            })
        # Sort: directories first, then files
        items.sort(key=lambda x: (not x['is_dir'], x['name'].lower()))
        
        return jsonify({
            "current_path": resolved,
            "parent_path": os.path.dirname(resolved) if resolved != WORK_DIR else None,
            "items": items,
            "root_path": WORK_DIR
        })
    except PermissionError:
        return jsonify({"error": "Permission denied"}), 403

@app.route('/api/upload', methods=['POST'])
def upload_file():
    path = request.form.get('path')
    if not path:
        return jsonify({"error": "Path required"}), 400
    resolved = _resolve_and_validate(path)
    if resolved is None:
        return jsonify({"error": "Invalid target path"}), 403
    
    if not os.path.isdir(resolved):
        return jsonify({"error": "Target path is not a directory"}), 400
        
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    try:
        # Save to target path (use secure filename)
        filename = secure_filename(file.filename)
        if not filename:
            return jsonify({"error": "Invalid filename after sanitization"}), 400
            
        save_path = os.path.join(resolved, filename)
        # Ensure target directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        file.save(save_path)
        return jsonify({"status": "success", "path": save_path})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/download', methods=['GET'])
def download_file():
    path = request.args.get('path')
    resolved = _resolve_and_validate(path)
    if not resolved or not os.path.exists(resolved):
        return jsonify({"error": "File not found"}), 404

    directory = os.path.dirname(resolved)
    filename = os.path.basename(resolved)
    return send_from_directory(directory, filename, as_attachment=True)

@app.route('/api/config', methods=['GET'])
def get_config():
    return jsonify(config_manager.get_config())

@app.route('/api/config', methods=['POST'])
def update_config():
    new_config = request.json
    config_manager.update_config(new_config)
    return jsonify({"status": "success"})

@app.route('/api/convert', methods=['POST'])
def convert():
    data = request.json
    input_file = data.get('file')
    resolved = _resolve_and_validate(input_file)
    if not resolved or not os.path.exists(resolved):
        return jsonify({"error": "File not found"}), 400
    
    success, message = encoder_service.start_encoding(resolved)
    if success:
        return jsonify({"status": "started", "message": message})
    else:
        return jsonify({"error": message}), 409

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify(encoder_service.get_status())

@app.route('/api/cancel', methods=['POST'])
def cancel():
    if encoder_service.cancel_encoding():
        return jsonify({"status": "cancelled"})
    else:
        return jsonify({"error": "No running process to cancel"}), 400

@app.route('/api/dpg/info', methods=['GET'])
def dpg_info():
    path = request.args.get('path')
    if not path:
        return jsonify({"error": "Path parameter is required"}), 400
    resolved = _resolve_and_validate(path)
    if not resolved or not os.path.exists(resolved):
        return jsonify({"error": "File not found"}), 404
        
    try:
        header = DpgHeader(resolved)
        return jsonify({
            "version": header.version,
            "frames": header.frames,
            "fps": header.fps,
            "audio_sample_rate": header.audioSampleRate,
            "audio_channels": header.audioCodecOrChannels, # 0=mp2, 1=gsm, 3=vorbis
            "video_size": header.videoSize,
            "audio_size": header.audioSize,
            "duration_seconds": header.frames / header.fps if header.fps > 0 else 0
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/dpg/preview', methods=['POST'])
def generate_preview():
    data = request.json
    path = data.get('path')
    if not path:
        return jsonify({"error": "Path parameter is required"}), 400
    resolved = _resolve_and_validate(path)
    if not resolved:
        return jsonify({"error": "Invalid path parameter"}), 400

    success, result = preview_service.generate_preview(resolved)
    if success:
        # Return URL relative to our new temp route
        return jsonify({"preview_url": f"/api/temp/{result}"})
    else:
        return jsonify({"error": result}), 500

@app.route('/api/temp/<path:filename>')
def serve_temp(filename):
    return send_from_directory(TEMP_DIR, filename)

@app.route('/api/dpg/thumbnail', methods=['GET'])
def get_thumbnail():
    path = request.args.get('path')
    if not path:
        return jsonify({"error": "Path parameter is required"}), 400
        
    resolved = _resolve_and_validate(path)
    if not resolved:
        return jsonify({"error": "Invalid path parameter"}), 400

    try:
        data, mimetype = thumbnail_service.get_thumbnail(resolved)
        if data is None:
            return jsonify({"error": "No thumbnail found"}), 404
            
        return data, 200, {'Content-Type': mimetype}
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/dpg/thumbnail', methods=['POST'])
def set_thumbnail():
    path = request.form.get('path')
    if not path:
        return jsonify({"error": "Path parameter is required"}), 400
        
    resolved = _resolve_and_validate(path)
    if not resolved:
        return jsonify({"error": "Invalid path parameter"}), 400
        
    if not os.path.isfile(resolved):
        return jsonify({"error": "Target is not a file"}), 400

    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
        
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    try:
        # Save uploaded file temporarily
        temp_dir = config_manager.get('GENERAL', 'other_temporary')
        os.makedirs(temp_dir, exist_ok=True)
            
        safe_filename = secure_filename(file.filename)
        if not safe_filename:
            return jsonify({"error": "Invalid image filename"}), 400
            
        temp_path = os.path.join(temp_dir, 'upload_thumb_' + safe_filename)
        file.save(temp_path)
        
        thumbnail_service.set_thumbnail(resolved, temp_path)
        
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host=host, port=5000)
