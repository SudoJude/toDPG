import os
import subprocess
import uuid
import builtins

# Mock gettext for dpg4x legacy code if not already mocked
if not hasattr(builtins, '_'):
    builtins._ = lambda x: x

from dpg4x.DpgHeader import DpgHeader

class PreviewService:
    def __init__(self, temp_dir):
        self.preview_dir = os.path.join(temp_dir, 'previews')
        if not os.path.exists(self.preview_dir):
            os.makedirs(self.preview_dir)

    def generate_preview(self, dpg_path, duration=30):
        """
        Generates an MP4 preview for the given DPG file.
        Returns the relative path to the preview file.
        """
        if not os.path.exists(dpg_path):
            return False, "File not found"

        try:
            header = DpgHeader(dpg_path)
            
            # Generate unique ID for this preview
            preview_id = str(uuid.uuid4())
            video_temp = os.path.join(self.preview_dir, f"{preview_id}.m1v")
            audio_temp = os.path.join(self.preview_dir, f"{preview_id}.mp2") # Assuming MP2 for now
            output_file = os.path.join(self.preview_dir, f"{preview_id}.mp4")

            # Extract streams
            with open(dpg_path, 'rb') as f:
                # Extract Audio
                f.seek(header.audioStart)
                # Calculate size for duration (approximate)
                # Audio size is total size. 
                # We can just extract a portion if we want, but for now let's try extracting enough for the duration.
                # But calculating bitrate might be tricky if not in header.
                # Header has sample rate and channels (or codec).
                # Let's just extract the whole audio stream or a reasonable chunk (e.g. 5MB)
                # If the file is huge, we don't want to read it all.
                # Let's read up to 5MB of audio and video, that should be enough for a preview.
                audio_chunk_size = min(header.audioSize, 5 * 1024 * 1024) 
                audio_data = f.read(audio_chunk_size)
                with open(audio_temp, 'wb') as af:
                    af.write(audio_data)

                # Extract Video
                f.seek(header.videoStart)
                video_chunk_size = min(header.videoSize, 20 * 1024 * 1024) # 20MB video
                video_data = f.read(video_chunk_size)
                with open(video_temp, 'wb') as vf:
                    vf.write(video_data)

            # Transcode with FFmpeg
            # DPG video is usually standard MPEG-1 video, so we let ffmpeg detect it.
            # We don't force rawvideo.
            
            cmd = [
                'ffmpeg',
                '-i', video_temp,
                '-i', audio_temp, # FFmpeg usually auto-detects MP2 audio
                '-c:v', 'libx264',
                '-preset', 'ultrafast',
                '-c:a', 'aac',
                '-t', str(duration),
                '-y',
                output_file
            ]

            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate()

            # Cleanup temp files
            if os.path.exists(video_temp):
                os.remove(video_temp)
            if os.path.exists(audio_temp):
                os.remove(audio_temp)

            if process.returncode != 0:
                return False, f"FFmpeg failed: {stderr.decode('utf-8')}"

            # Return relative path for URL
            return True, f"previews/{preview_id}.mp4"

        except Exception as e:
            return False, str(e)
