"""
DPG file header: binary layout, reading, and writing.

    DPG0-1 Header size 36
        0-3: 'DPGX' where X is the version
        4-7: Number of frames in the video
        8-11: FPS
        12-15: Audio sample rate
        16-19: Number of audio channels (special values for gsm:1/ogg:3)
        20-23: Audio start
        24-27: Audio size
        28-31: Video start
        32-35: Video size

    DPG2-3 additional GOP header, +12 = 48 bytes total
        36-39: GOP start
        40-43: GOP size
        44-47: Pixel format (DPG1 writes this at byte 36)

    DPG4 additional thumbnail marker, +4 = 52 bytes total
        48-51: 'THM0'
        Thumbnail image immediately follows, fixed size 98304 bytes
        (256 x 192, 16-bit RGB1555)

Video stream: MPEG-1, 256x192, typically 15-30 fps.
Audio stream: MP2 (gsm/vorbis also supported by the format), typically
32000 Hz / 128 kbps.
"""
import struct

THUMBNAIL_WIDTH = 256
THUMBNAIL_HEIGHT = 192
THUMBNAIL_SIZE_BYTES = THUMBNAIL_WIDTH * THUMBNAIL_HEIGHT * 2  # RGB1555, 16 bits/px

# audioCodecOrChannels values
AUDIO_CODEC_MP2 = 0
AUDIO_CODEC_GSM_MONO = 1
AUDIO_CODEC_GSM_STEREO = 2
AUDIO_CODEC_VORBIS = 3

# pixelFormat values
PIXEL_FORMAT_RGB15 = 0
PIXEL_FORMAT_RGB18 = 1
PIXEL_FORMAT_RGB21 = 2
PIXEL_FORMAT_RGB24 = 3


class DpgHeaderError(Exception):
    pass


class DpgHeader:
    """Reads and writes the binary header of a DPG (0-4) file."""

    def __init__(self, filename=None):
        self.version = None
        self.frames = 0
        self.fps = 0
        self.audioSampleRate = 0
        self.audioCodecOrChannels = 0
        self.audioStart = 0
        self.audioSize = 0
        self.videoStart = 0
        self.videoSize = 0
        self.gopStart = 0
        self.gopSize = 0
        self.pixelFormat = 0
        self.hasThumb = False
        if filename:
            self.fromFile(filename)

    def __str__(self):
        pixel_names = {
            PIXEL_FORMAT_RGB15: "RGB15",
            PIXEL_FORMAT_RGB18: "RGB18",
            PIXEL_FORMAT_RGB21: "RGB21",
            PIXEL_FORMAT_RGB24: "RGB24",
        }
        p_format = pixel_names.get(self.pixelFormat, "RGB24")

        a_channels = 2
        if self.audioCodecOrChannels == AUDIO_CODEC_MP2:
            a_codec = "mp2"
        elif self.audioCodecOrChannels == AUDIO_CODEC_VORBIS:
            a_codec = "vorbis"
        elif self.audioCodecOrChannels in (AUDIO_CODEC_GSM_MONO, AUDIO_CODEC_GSM_STEREO):
            a_codec = "libgsm"
            a_channels = self.audioCodecOrChannels
        else:
            a_codec = "unknown"

        lines = [
            f"DPG Version: {self.version}",
            "Video Codec: mpeg1",
            f"Frames Per Second: {self.fps}",
            f"Pixel Format: {p_format}",
            f"Video Size: {self.videoSize} bytes, {self.frames} frames",
            "",
            f"Audio Codec: {a_codec}",
            f"Audio Frequency: {self.audioSampleRate}, {a_channels} channels",
            f"Audio Size: {self.audioSize} bytes",
            "",
            f"GOP Size: {self.gopSize} bytes",
        ]
        if self.hasThumb:
            lines.append("Embedded Thumbnail")
        return "\n".join(lines)

    @staticmethod
    def getVersionFromFile(filename):
        with open(filename, "rb") as fd:
            version_hdr = fd.read(4)
        if version_hdr[:3] != b"DPG":
            return None
        return version_hdr[3] - ord("0")

    def setSizes(self, version, vSize, aSize, gSize=0):
        """Set version and stream sizes; recalculates start offsets."""
        self.version = version
        self.videoSize = vSize
        self.audioSize = aSize
        self.gopSize = gSize

        self.audioStart = 36
        if version in (2, 3):
            self.audioStart += 12
        elif version >= 4:
            self.hasThumb = True
            self.audioStart += 12 + 4 + THUMBNAIL_SIZE_BYTES

        self.videoStart = self.audioStart + self.audioSize
        self.gopStart = self.videoStart + self.videoSize

    def setAudio(self, codec="mp2", sampleRate=32000):
        if codec == "libgsm":
            # GSM is always mono in this encoder.
            self.audioCodecOrChannels = AUDIO_CODEC_GSM_MONO
        elif codec == "mp2":
            self.audioCodecOrChannels = AUDIO_CODEC_MP2
        elif codec == "vorbis":
            self.audioCodecOrChannels = AUDIO_CODEC_VORBIS
        else:
            raise DpgHeaderError(f"{codec!r} is not a valid DPG audio codec")
        self.audioSampleRate = sampleRate

    def setVideo(self, frames, fps=15, pixel=PIXEL_FORMAT_RGB24):
        self.frames = frames
        self.fps = fps
        self.pixelFormat = pixel

    def fromFile(self, filename):
        with open(filename, "rb") as fd:
            version_str = fd.read(4)
            if version_str[:3] != b"DPG":
                raise DpgHeaderError(f"{filename} is not a valid DPG file")
            self.version = version_str[3] - ord("0")
            self.frames = struct.unpack("<l", fd.read(4))[0]
            fd.read(1)  # reserved
            self.fps = struct.unpack("<b", fd.read(1))[0]
            fd.read(2)  # reserved
            self.audioSampleRate = struct.unpack("<l", fd.read(4))[0]
            self.audioCodecOrChannels = struct.unpack("<l", fd.read(4))[0]
            self.audioStart = struct.unpack("<l", fd.read(4))[0]
            self.audioSize = struct.unpack("<l", fd.read(4))[0]
            self.videoStart = struct.unpack("<l", fd.read(4))[0]
            self.videoSize = struct.unpack("<l", fd.read(4))[0]

            if self.version > 1:
                self.gopStart = struct.unpack("<l", fd.read(4))[0]
                self.gopSize = struct.unpack("<l", fd.read(4))[0]
            if self.version > 0:
                self.pixelFormat = struct.unpack("<l", fd.read(4))[0]
            if self.version > 3:
                thumb_marker = fd.read(4)
                self.hasThumb = thumb_marker == b"THM0"

    def toFile(self, filename):
        with open(filename, "wb") as fd:
            fd.write(struct.pack("4s", b"DPG%i" % self.version))
            fd.write(struct.pack("<l", self.frames))
            fd.write(struct.pack("<b", 0))
            fd.write(struct.pack("<b", self.fps))
            fd.write(struct.pack("<h", 0))
            fd.write(struct.pack("<l", self.audioSampleRate))
            fd.write(struct.pack("<l", self.audioCodecOrChannels))
            fd.write(struct.pack("<l", self.audioStart))
            fd.write(struct.pack("<l", self.audioSize))
            fd.write(struct.pack("<l", self.videoStart))
            fd.write(struct.pack("<l", self.videoSize))

            if self.version >= 2:
                fd.write(struct.pack("<l", self.gopStart))
                fd.write(struct.pack("<l", self.gopSize))
            if self.version > 0:
                fd.write(struct.pack("<l", self.pixelFormat))
            if self.version == 4:
                fd.write(struct.pack("4s", b"THM0"))
