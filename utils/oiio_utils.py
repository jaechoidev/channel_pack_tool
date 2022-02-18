'''
oiio_utils.py

This is to get basic functions using open image io.
'''

from PySide6 import QtCore, QtWidgets, QtGui
import OpenImageIO as oiio 
from OpenImageIO import ImageInput, ImageOutput
from OpenImageIO import ImageBuf, ImageSpec, ImageBufAlgo

def open_image_file(filename):
    input_data = oiio.ImageInput.open(filename)
    if not input_data:
        print ('Could not open %s "' % input_image)
        print ("\tError: ", oiio.geterror())
        return
    spec = input_data.spec()
    pixels = input_data.read_image()
    input_data.close()
    return pixels, spec


def get_colorspace_from_imgbuf(imgbuf):
    colorspace = imgbuf.spec().getattribute('oiio:ColorSpace')
    if not colorspace:
        pass # todo : check file type
    return colorspace


def get_colorspace_from_filepath(filename):
    imgbuf = ImageBuf(filename)
    return get_colorspace_from_imgbuf(imgbuf)


def get_channel(imgbuf, channel):
    channel_buf = ImageBuf()
    ImageBufAlgo.channels(channel_buf, imgbuf, (channel,))
    return channel_buf


def split_channels(imgbuf):
    pass


def get_pixmap_from_imgbuf(imgbuf):
    pixels = imgbuf.get_pixels(oiio.UINT8)
    h, w, nchannels = pixels.shape
    if nchannels == 1:
        img = QtGui.QImage(pixels, w, h, w*nchannels, QtGui.QImage.Format_Grayscale8)
    else:
        img = QtGui.QImage(pixels, w, h, w*nchannels, QtGui.QImage.Format_RGB888)
    return QtGui.QPixmap.fromImage(img)
    