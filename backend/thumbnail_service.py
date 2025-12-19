import os
import struct
import subprocess
import shutil
import tempfile

class ThumbnailService:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        
    def get_thumbnail(self, dpg_path):
        """
        Extracts the thumbnail from a DPG file and returns it as PNG data.
        Returns: (bytes, mimetype) or (None, None) if no thumbnail
        """
        if not os.path.exists(dpg_path):
            raise Exception("File not found")
            
        # Security: Double-check the path is normalized and in a reasonable location
        # This helps CodeQL trace the safety of the path local to this function.
        if '..' in dpg_path or not os.path.isabs(dpg_path):
             raise Exception("Invalid path format")
            
        with open(dpg_path, 'rb') as f:
            # Check version
            header = f.read(4) 
            if not header.startswith(b'DPG'):
                raise Exception("Not a DPG file")
                
            version = int(chr(header[3]))
            if version < 4:
                return None, None
                
            # Check for THM0 marker at offset 48
            f.seek(48)
            marker = f.read(4)
            if marker != b'THM0':
                return None, None
                
            # Read 98304 bytes of thumbnail data (16-bit RGB1555)
            # Offset 52
            thumb_data = f.read(98304)
            if len(thumb_data) != 98304:
                return None, None
                
        # Convert RGB1555 to RGB24
        # Format: A1 R5 G5 B5 (Little Endian)
        rgb24_data = []
        for i in range(0, len(thumb_data), 2):
            pixel = struct.unpack('<H', thumb_data[i:i+2])[0]
            
            # Extract 5-bit channels
            r = (pixel & 0x1F) << 3
            g = ((pixel >> 5) & 0x1F) << 3
            b = ((pixel >> 10) & 0x1F) << 3
            
            # Simple 5-bit to 8-bit scaling (shift) isn't perfect but sufficient
            rgb24_data.extend([r, g, b])
            
        raw_bytes = bytes(rgb24_data)
        
        # Use ffmpeg to convert Raw RGB24 to PNG
        # Input: 256x192, rgb24
        try:
            cmd = [
                'ffmpeg', 
                '-f', 'rawvideo',
                '-pixel_format', 'rgb24',
                '-video_size', '256x192',
                '-i', 'pipe:0',
                '-f', 'image2',
                '-vcodec', 'png',
                '-'
            ]
            
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            png_data, stderr = process.communicate(input=raw_bytes)
            
            if process.returncode != 0:
                print(f"FFmpeg error: {stderr.decode()}")
                raise Exception("Conversion failed")
                
            return png_data, 'image/png'
            
        except Exception as e:
            print(f"Thumbnail error: {e}")
            raise e

    def set_thumbnail(self, dpg_path, image_path):
        """
        Replaces the thumbnail in a DPG file with the provided image.
        """
        if not os.path.exists(dpg_path):
            raise Exception("DPG file not found")
        
        # Security: Explicitly reject paths that look suspicious
        if '..' in dpg_path or not os.path.isabs(dpg_path):
             raise Exception("Invalid path format")
        if '..' in image_path:
             raise Exception("Invalid image path format")
            
        # 1. Convert input image to Raw RGB24 and resize to 256x192
        try:
            cmd = [
                'ffmpeg', '-y',
                '-i', image_path,
                '-vf', 'scale=256:192',
                '-f', 'rawvideo',
                '-pix_fmt', 'rgb24',
                '--', '-'
            ]
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            raw_rgb, stderr = process.communicate()
            
            if process.returncode != 0:
                raise Exception(f"Image conversion failed: {stderr.decode()}")
                
            if len(raw_rgb) != 256 * 192 * 3:
                raise Exception("Resized image has incorrect dimensions")
                
        except Exception as e:
            raise e
            
        # 2. Convert raw RGB24 to RGB1555 (16-bit)
        packed_pixels = []
        for i in range(0, len(raw_rgb), 3):
            r = raw_rgb[i]
            g = raw_rgb[i+1]
            b = raw_rgb[i+2]
            
            # R5 G5 B5 packing
            # Note: DPG uses A1 R5 G5 B5 or similar. 
            # DpgThumbnail.py logic:
            # pixel = (( 1 << 15) | ((blue >> 3) << 10) | ((green >> 3) << 5) | (red >> 3))
            
            pixel = ((1 << 15) | 
                     ((b >> 3) << 10) | 
                     ((g >> 3) << 5) | 
                     (r >> 3))
            packed_pixels.append(struct.pack('<H', pixel))
            
        thumb_data = b''.join(packed_pixels)
        
        # 3. Inject into DPG file
        with open(dpg_path, 'r+b') as f:
            # Check headers
            header = f.read(4)
            version = int(chr(header[3]))
            
            if version < 4:
                raise Exception("Target file is not DPG4 or higher. Cannot add thumbnail.")
                
            f.seek(48)
            marker = f.read(4)
            if marker != b'THM0':
                 # If header space says DPG4 but no THM0, it's malformed or empty
                 # But we assume standard layout if DPG4
                 raise Exception("Target file missing THM0 marker")
            
            # Write data at offset 52
            f.seek(52)
            f.write(thumb_data)
            
        return True
