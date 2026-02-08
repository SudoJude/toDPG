# -*- coding: utf-8 -*-
'''
Created on 16 sep 2012

@author: Marc P. Davignon
         minor updates by Tomas Aronsson

Class to handle DPG thumbnails:
 - Extract from an image file, including rescaling 
 - Extract from a DPG file
 - Reformat into a DPG thumbnail that can be included in a DPG4 file
'''

import os
import struct
import shutil

from PIL import Image
import wx

from dpg4x.DpgHeader import DpgHeader

class DpgThumbnail(object):
    '''
    classdocs
    '''   
    def __init__(self, src = None):
        '''
        Constructor
        '''
        self.img = None
        self.src = src
        # All DPG thumbnails have this size
        self.size = wx.Size(256, 192)
        if src is not None:
            self.fromFile(src)
        
    def __str__(self):
        return "DpgThumbnail: src=%s" % self.src
    
    def getImage(self):
        return self.img
    
    def getThumbData(self):
        '''Convert the image to the thumbnail format
        
        To create a file readable by an image viewer:
        tga16_file = open('thumb.tga', 'wb')
        tga_header=b'\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xC0\x00\x10\x00'
        tga16_file.write(tga_header)
        tga16_file.write(thumb_data) 
        tga16_file.close()
        '''
        # The final image should have these dimensions
        dest_w, dest_h = self.size
        # Process every pixel in the image
        data = []
        for i in range(dest_h):
            row = []
            for j in range(dest_w):
                # Get the RGB values
                red = self.img.GetRed(j, i)
                green = self.img.GetGreen(j, i)
                blue = self.img.GetBlue(j, i)
                # Recombine the pixel value in 16 bit mode
                pixel = (( 1 << 15)
                         | ((blue >> 3) << 10)
                         | ((green >> 3) << 5)
                         | (red >> 3))
                # Add the pixel to the current row
                row.append(pixel)
            # Append the row to the data
            data.append(row)
        # Join all the data with the desired format
        row_fmt=('H'*dest_w)
        return b''.join(struct.pack(row_fmt, *row) for row in data)

    def inject(self, inputN, outputN = None):
        # Variables used on error handling, they need to be declared
        fdOutput = None

        try:
            if not (os.path.isfile(inputN) and (os.access(inputN, os.R_OK))):
                raise Exception(_('ERROR: The file %s cannot be read') % inputN)

            if outputN is None:
                outputN = inputN
            outPath = os.path.dirname(outputN)
            outPath = os.path.abspath(outPath)
            if (os.path.isfile(outputN) and (not os.access(outputN, os.W_OK))):
                raise Exception(_('ERROR: The file %s cannot be written') % outputN)
            if not os.access(outPath, os.W_OK):
                raise Exception(_('ERROR: The folder %s cannot be written') % outPath)

            dpgVersion = DpgHeader.getVersionFromFile(inputN)
            if dpgVersion:
                # Use a specific message if DPG version < 4
                # Todo: it could be possible to upgrade to DPG4 but
                # leads to more complicated code because header size grows
                if dpgVersion < 4:
                    raise Exception(_('%(file)s is a DPG version %(version)s ' \
                                      'file, but version 4 or better is required') % 
                                    {"file": inputN, "version": dpgVersion})
            else:
                raise Exception(_('%s is not a valid DPG file') % inputN)

            # Copy file if not modifying input
            if (outputN != inputN):
                shutil.copyfile(inputN, outputN)

            fdOutput = open(outputN, 'r+b')
            # DPG0-3 Header size 36
            # DPG4 Header size 36 + 4 (THM0) = 40
            # DPG2-4 GOP Header +12 = 48 (DPG2-3) or 52 (DPG4)
            # Image Size is 98304
            # Audio start 52 + 98304 = 98356

            fdOutput.seek(52, os.SEEK_SET)
            fdOutput.write(self.getThumbData())
        finally:
            if fdOutput:
                fdOutput.close()
       
    def fromFile(self, filename):
        """ Reads a thumbnail from a DPG or image file"""
        dpgVersion = DpgHeader.getVersionFromFile(filename)
        if dpgVersion is not None:
            # Use a specific message if DPG version < 4
            if dpgVersion < 4:
                raise Exception(_('%(file)s is a DPG version %(version)s ' \
                                  'file, but version 4 or better is required') % 
                                  {"file": filename, "version": dpgVersion})
            else:
                self.__fromDpgFile(filename)
        else:
            self.__fromImgFile(filename)
        
        
    def __fromDpgFile(self, filename):
        """ Reads a thumbnail from a DPG file and unpacks into a wx image"""

        fd = open(filename, 'rb')
        fd.seek(48, os.SEEK_SET)
        thumbStr = fd.read(4)
        # Can ver4 exist without this? Or would it be a corrupt file?
        if thumbStr != b'THM0':
            raise Exception(_('%s is not a valid DPG file') % filename)
        dest_w, dest_h = self.size

        d = fd.read(98304)
        # debug code to verify that thumbnails can be packed and unpacked
        # d = self.getThumbData()
        self.img = wx.Image(dest_w, dest_h)
        for i in range(dest_h):
            for j in range(dest_w):
                p = (i * dest_w + j) * 2
                pixel = struct.unpack("H", d[p:p+2])[0]
                r = (pixel & 31) << 3 
                g = (pixel & (31 << 5)) >> 2
                b = (pixel & (31 << 10)) >> 7
                # print i,j,p, len(d), r, g, b
                self.img.SetRGB(j, i, r,g,b)        
        fd.close()
        self.src = filename     

    
    def __fromImgFile(self, imgFile):
        """ Reads an image from a file and scales it to the thumbnail size"""
        # The final image should have these dimensions
        dest_w, dest_h = self.size

        # PIL supports an high-quality antialiased downsampling function.
        # Hard to predict when PIL closes a file
        # pilImage = Image.open(thumbfile), causes problems on Windows
        fp = open(imgFile, "rb")
        pilImage = Image.open(fp) # open from file object
        pilImage.load() # make sure PIL has read the data
        fp.close()
        width, height = pilImage.size
        self.src = imgFile

        # Test to see if the image needs to be resized
        if (width == dest_w and height == dest_h):
            self.img = wx.Image(imgFile)
        else:
            # Find and keep the image aspect ratio
            ratio = round(float(width) / float(height), 2)
            nwidth = 256
            nheight = int(256.0/ratio+0.5)
            nxpos = 0
            nypos = (192-nheight)/2
            # When height is greater than the screen max, scale down width instead
            if nheight > 192:
                nwidth = int(192.0*ratio+0.5)
                nheight = 192
                nxpos = (256-nwidth)/2
                nypos = 0

            # First, Rescale/Resize the thumbnail keeping the original aspect ratio
            pilImage = pilImage.resize((nwidth, nheight),Image.ANTIALIAS)
            # Convert a PIL (the Python Image Library format) object to a wxPython
            # Image (or Bitmap) while keeping the alpha transparency layer.
            image = wx.Image(pilImage.size[0],pilImage.size[1])
            image.SetData(pilImage.convert("RGB").tobytes())
            image.SetAlpha(pilImage.convert("RGBA").tobytes()[3::4])

            # Second, Resize to the default screen size adding borders as necessary
            self.img = image.Resize(self.size, wx.Point(nxpos,nypos))
