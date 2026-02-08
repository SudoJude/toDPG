import os
import sys
import shutil

# Application Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORK_DIR = '/app/work'
TEMP_DIR = os.path.join(WORK_DIR, 'tmp')
USER_HOME = os.path.expanduser("~")
CONFIG_DIR = os.path.join(WORK_DIR, ".dpg4x-web")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.ini")

# Ensure config directory exists
if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_DIR)

# Copy test files to use as a reference
s = '/app/test'
files = os.listdir(s)

for fname in files:
    shutil.copy(os.path.join(s, fname), WORK_DIR)

# Default Configuration
DEFAULT_CONFIG = {
    'GENERAL': {
        'dpg_version': '4',
        'dpg_quality': 'normal',
        'other_output' : WORK_DIR,
        'other_temporary': TEMP_DIR,
        'other_previewsize': '10',
    },
    'VIDEO': {
        'video_keepaspect': 'True',
        'video_width': '256',
        'video_height': '192',
        'video_bitrate': '256',
        'video_fps': '24',
        'video_autofps': 'True',
        'video_pixel': '0', # 0=rgb15, 1=rgb18, 2=rgb21, 3=rgb24
    },
    'AUDIO': {
        'audio_codec': 'mp2',
        'audio_bitrate_mp2': '128',
        'audio_bitrate_vorbis': '128',
        'audio_frequency': '32000',
        'audio_normalize': 'False',
        'audio_mono': 'False',
    },
    'SUBTITLES': {
        'subtitles_source': 'disable', # disable, sid, file
        'subtitles_track': '0',
        'subtitles_file': '',
        'subtitles_font': '',
        'subtitles_encoding': 'utf-8',
    }
}

def get_platform_shell():
    return sys.platform == 'win32'
