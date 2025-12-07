from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import os
from backend.config_manager import ConfigManager
from backend.config_manager import ConfigManager
from backend.encoder_service import EncoderService
from backend.preview_service import PreviewService
from backend.thumbnail_service import ThumbnailService
from backend.globals import WORK_DIR
import builtins

# Mock gettext for dpg4x legacy code
builtins._ = lambda x: x

from dpg4x.DpgHeader import DpgHeader

app = Flask(__name__, static_folder='static')
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024  # 1 Gigabyte
CORS(app) # Enable CORS for Angular frontend

config_manager = ConfigManager()
encoder_service = EncoderService(config_manager)
preview_service = PreviewService(app.static_folder)
thumbnail_service = ThumbnailService(config_manager)

@app.route('/api/files', methods=['GET'])
def list_files():
    path = request.args.get('path', WORK_DIR)
    
    # Security check: Ensure path is within WORK_DIR
    if not path.startswith(WORK_DIR):
        path = WORK_DIR
        
    if not os.path.exists(path):
        return jsonify({"error": "Path does not exist"}), 404

    # Ensure WORK_DIR exists
    if not os.path.exists(WORK_DIR):
        os.makedirs(WORK_DIR)
    
    try:
        items = []
        for entry in os.scandir(path):
            items.append({
                "name": entry.name,
                "path": entry.path,
                "is_dir": entry.is_dir(),
                "size": entry.stat().st_size if not entry.is_dir() else 0
            })
        # Sort: directories first, then files
        items.sort(key=lambda x: (not x['is_dir'], x['name'].lower()))
        
        return jsonify({
            "current_path": path,
            "parent_path": os.path.dirname(path) if path != WORK_DIR else None,
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
        
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    try:
        # Save to target path
        save_path = os.path.join(path, file.filename)
        file.save(save_path)
        return jsonify({"status": "success", "path": save_path})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/download', methods=['GET'])
def download_file():
    path = request.args.get('path')
    if not path or not os.path.exists(path):
        return jsonify({"error": "File not found"}), 404
        
    if not path.startswith(WORK_DIR):
        return jsonify({"error": "Access denied"}), 403
        
    return send_file(path, as_attachment=True)

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
    if not input_file or not os.path.exists(input_file):
        return jsonify({"error": "File not found"}), 400
    
    success, message = encoder_service.start_encoding(input_file)
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
    
    if not os.path.exists(path):
        return jsonify({"error": "File not found"}), 404
        
    try:
        header = DpgHeader(path)
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
    
    success, result = preview_service.generate_preview(path)
    if success:
        # Return full URL or relative path that frontend can use
        # Assuming frontend is served from same domain/port or proxy handles it.
        # For dev, we might need full URL if ports differ.
        # But let's return relative path and let frontend handle base URL.
        return jsonify({"preview_url": f"/static/{result}"})
    else:
        return jsonify({"error": result}), 500

@app.route('/api/dpg/thumbnail', methods=['GET'])
def get_thumbnail():
    path = request.args.get('path')
    if not path:
        return jsonify({"error": "Path parameter is required"}), 400
        
    try:
        data, mimetype = thumbnail_service.get_thumbnail(path)
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
        
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
        
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    try:
        # Save uploaded file temporarily
        temp_dir = config_manager.get('GENERAL', 'other_temporary')
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
            
        temp_path = os.path.join(temp_dir, 'upload_thumb_' + file.filename)
        file.save(temp_path)
        
        thumbnail_service.set_thumbnail(path, temp_path)
        
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    app.run(debug=True, host=host, port=5000)
