# -*- coding: utf-8 -*-
'''
Created on 9 sep 2012

@author: Félix Medrano Sanz
         minor updates by Tomas Aronsson
'''
import struct

"""
 DPG Header

The DPG file starts with a header:

    DPG0-1 Header size 36
        0-3: 'DPGX' where X is the version
        4-7: Number of frames in the video
        8-11: FPS
        12-15: Audio sample rate
        16-19: Number of audio channels (special for gsm:1/ogg:3)
        20-23: Audio start
        24-27: Audio size
        28-31: Video start
        32-35: Video size 

    DPG2-3 additional GOP Header +12 = 48 (DPG2-3) or 52 (DPG4)
        36-39: GOP start
        40-43: GOP size
        44-47: Pixel format (DPG1 writes this information at byte 36) 

    DPG4: Thumbnail pictures,
        48-51 'THM0'
        Thumbnail image size is 98304
        Audio start 52 + 98304 = 98356 

 Codecs

Video stream:

    Codec - mpeg1
    Height - 192, could theoretically be as low as 16
    Width - 256
    FPS - 15 

Audio stream:

    Codec - mp2, gsm/ogg also possible
    Bitrate 128
    Sample rate 32000, higher possible but may result in worse quality 

Thumbnail:

    Codec - TGA, without header, 16 bit RGB values
    Height - 192
    Width - 256 
"""
class DpgHeader():
    def __init__(self, filename = None):
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
        s = _('DPG Version') + ': %d\n' % self.version
        s += _('Video Codec') + ': mpg1\n'
        s += _('Frames Per Second') + ': %d\n' % self.fps
        
        if self.pixelFormat == 0:
            pFormat = 'RGB15'
        elif self.pixelFormat == 1:
            pFormat = 'RGB18'
        elif self.pixelFormat == 2:
            pFormat = 'RGB21'
        else:
            pFormat = 'RGB24'
            
        s += _('Pixel Format') + ': %s\n' % pFormat
        s += _('Size: %d bytes') % self.videoSize
        s += ', %d ' % self.frames + _('frames') + '\n'
        s += '\n'

        # Number of audio channels, has special values for MP2 and OGG Vorbis
        aChannels = 2
        if self.audioCodecOrChannels == 0:
            aCodec = 'mp2'
        elif self.audioCodecOrChannels == 3:
            aCodec = 'vorbis'
        elif self.audioCodecOrChannels == 1 or self.audioCodecOrChannels == 2:
            aCodec = 'libgsm'
            aChannels = self.audioCodecOrChannels
        else:
            aCodec = _('unknown')

        s += _('Audio Codec') + ': %s\n' % aCodec
        s += _('Audio Frequency') + ': %d, ' % self.audioSampleRate
        s += '%d ' % aChannels + _('channels') + '\n'
        s += _('Size: %d bytes') % self.audioSize
        s += '\n\n'
        s += _('GOP') + ' '
        s += _('Size: %d bytes') % self.gopSize
        if self.hasThumb:
            s += '\n' + _('Embedded Thumbnail')
        return s

    @staticmethod
    def getVersionFromFile(file):
        fd = open(file, 'rb')
        # Read the DPG version
        versionHdr = fd.read(4)
        fd.close()
        if versionHdr[:3] != b'DPG':
            return None
        version = versionHdr[3] - ord('0')
        return version


    def setSizes(self, version, vSize, aSize, gSize = 0):
        """Sets version and sizes, start positions will be recalculated"""
        self.version = version
        self.videoSize = vSize
        self.audioSize = aSize
        self.gopSize = gSize

        # Calculate the start of the audio file
        self.audioStart = 36
        # DPG2 and DPG3 include also the GOP header
        if (self.version == 2) or (self.version == 3):
            self.audioStart += 12
        # DPG4 includes also a thumbnail
        elif self.version >= 4:
            self.hasThumb = True
            # The thumbnail is always 98320 bytes
            self.audioStart += 98320
        self.videoStart = self.audioStart + self.audioSize
        self.gopStart = self.videoStart + self.videoSize
                    
    def setAudio(self, codec = "mp2", sampleRate = 32000):
        # Number of audio channels, has special values for MP2 and OGG Vorbis
        if codec == 'libgsm':
            # Yes, always mono audio. I was not able to encode stereo GSM
            self.audioCodecOrChannels = 1
        # Mp2 is the default
        elif codec == 'mp2':
            self.audioCodecOrChannels = 0
        elif codec == 'vorbis':
            self.audioCodecOrChannels = 3
        else: 
            raise Exception(_('%s is not a valid DPG audio codec') % codec)
        # Sample rate 32000, higher possible but may result in worse quality
        self.audioSampleRate = sampleRate
    
    def setVideo(self, frames, fps = 15, pixel = 3):
        self.frames = frames
        self.fps = fps
        # DPG0 only supports the RGB24 pixel format (value=3), other formats
        # have caused problems in mencoder
        self.pixelFormat = pixel
    
    def fromFile(self, filename):
        fd = open(filename, 'rb')
        versionStr = fd.read(4)
        if versionStr[:3] != b'DPG':
            raise Exception(_('%s is not a valid DPG file') % filename)
        self.version = versionStr[3] - ord('0')
        self.frames = struct.unpack("<l", fd.read(4))[0]
        # FPS only using one byte
        fd.read(1)
        self.fps = struct.unpack("<b", fd.read(1))[0]
        fd.read(2)
        self.audioSampleRate = struct.unpack("<l", fd.read(4))[0]
        self.audioCodecOrChannels =  struct.unpack("<l", fd.read(4))[0]
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
            thumbStr = fd.read(4)
            # Can ver4 exist without this? Or would it be a corrupt file?
            self.hasThumb = (thumbStr == 'THM0')
        fd.close()
             

    def toFile(self, filename):
        fd = open(filename, 'wb')

        # The header starts with 4 bytes with DPGX, being X the version
        fd.write(struct.pack ( "4s" , b"DPG%i" % self.version))
        # The initial header part is the same in all versions
        fd.write(struct.pack ( "<l" , self.frames))
        fd.write(struct.pack ( "<b" , 0))
        fd.write(struct.pack ( "<b" , self.fps))
        fd.write(struct.pack ( "<h" , 0))
        fd.write(struct.pack ( "<l" , self.audioSampleRate))
        fd.write(struct.pack ( "<l" , self.audioCodecOrChannels))
        fd.write(struct.pack ( "<l" , self.audioStart))
        fd.write(struct.pack ( "<l" , self.audioSize))
        fd.write(struct.pack ( "<l" , self.videoStart))
        fd.write(struct.pack ( "<l" , self.videoSize))

        # For DPG >= 2, add the GOP file
        # This information allows faster seeking
        if self.version >= 2:
            fd.write(struct.pack ( "<l" , self.gopStart))
            fd.write(struct.pack ( "<l" , self.gopSize))
        # Add the pixel format
        # DPG0 only supports the RGB24 pixel format and does not have this
        # I have problems with other pixel formats and mencoder anyway
        if self.version > 0:
            fd.write(struct.pack ( "<l" , self.pixelFormat))
        # Thumbnail header for DPG4
        if self.version == 4:
            fd.write(struct.pack ( "4s" , b"THM0"))
        fd.close()
