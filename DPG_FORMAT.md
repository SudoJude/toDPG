# DPG Video Format Specification (Version 4)

DPG (NPG) is a video format designed for the Nintendo DS, specifically for the Moonshell media player.

## File Structure

A DPG4 file consists of:
1.  **Header** (52 bytes)
2.  **Thumbnail Data** (98304 bytes)
3.  **Audio Stream** (MP2)
4.  **Video Stream** (MPEG-1 Video)
5.  **GOP Table** (Optional index for seeking)

## Header Format (Little Endian)

| Offset | Size | Type | Description |
|--------|------|------|-------------|
| 0 | 4 | char[4] | "DPG4" (Magic / Version) |
| 4 | 4 | uint32 | Total Frames |
| 8 | 1 | uint8 | Reserved (0) |
| 9 | 1 | uint8 | FPS (Frames Per Second) |
| 10 | 2 | uint16 | Reserved (0) |
| 12 | 4 | uint32 | Audio Frequency (e.g. 32000) |
| 16 | 4 | uint32 | Audio Channels / Codec ID |
| 20 | 4 | uint32 | Audio Stream Start Offset |
| 24 | 4 | uint32 | Audio Stream Size (bytes) |
| 28 | 4 | uint32 | Video Stream Start Offset |
| 32 | 4 | uint32 | Video Stream Size (bytes) |
| 36 | 4 | uint32 | GOP Table Start Offset |
| 40 | 4 | uint32 | GOP Table Size (bytes) |
| 44 | 4 | uint32 | Pixel Format (3 = RGB24) |
| 48 | 4 | char[4] | "THM0" (Thumbnail Marker) |

## Thumbnail

- **Location**: Immediately follows the header (Offset 52).
- **Marker**: The header must end with `THM0`.
- **Dimensions**: 256 x 192 pixels.
- **Format**: 16-bit RGB1555 (A1 R5 G5 B5).
- **Size**: 256 * 192 * 2 = 98304 bytes.

### Pixel Packing (A1 R5 G5 B5)
Each pixel is a 16-bit integer (Little Endian):
`BIT 15`: Alpha / Unused (Set to 1)
`BITS 14-10`: Blue (5 bits)
`BITS 9-5`: Green (5 bits)
`BITS 4-0`: Red (5 bits)

## Streams

### Audio
- **Codec**: MP2 (MPEG-1 Audio Layer II)
- **Standard**: 32000 Hz, 2 Channels, 128 kbps.

### Video
- **Codec**: MPEG-1 Video
- **Resolution**: 256x192
- **Framerate**: Typically 20, 24, or 30 fps.
- **Bitrate**: Variable, typically ~256 kbps.
- **Note**: The video stream is standard MPEG-1, but enclosed within the DPG container.
