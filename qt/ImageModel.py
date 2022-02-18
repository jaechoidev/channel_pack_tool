"""
ImageViewModel.py
"""

import sys, os, cv2
import numpy as np
from PySide6 import QtCore, QtWidgets, QtGui
import OpenImageIO as oiio 
from OpenImageIO import ImageInput, ImageOutput
from OpenImageIO import ImageBuf, ImageSpec, ImageBufAlgo
from utils.oiio_utils import open_image_file

class Communicate(QtCore.QObject):
    changed = QtCore.Signal()
    clicked = QtCore.Signal()


class ImageModel(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        self.signal = Communicate()
        self.pressed = False
        self.setStyleSheet("QLabel{border: 1px dashed #aaa}")

    def mousePressEvent(self, e):
        self.pressed = True

    def mouseReleaseEvent(self, e):
        if self.pressed:
            self.signal.clicked.emit()
            self.pressed = False

    def openFile(self, filename):
        input_data = oiio.ImageInput.open(filename)
        if not input_data:
            print ('Could not open %s "' % input_image)
            print ("\tError: ", oiio.geterror())
            return
        spec = input_data.spec()
        #pixels = input_data.read_image(format='int8')
        pixels = input_data.read_image()
        input_data.close()
        return pixels

    def set_image(self, rgba):
        pixels = rgba.get_pixels(oiio.UINT8)
        h, w, _ = pixels.shape
        img = QtGui.QImage(pixels, w, h, 3 * w, QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(img)
        self.pix = pix.scaled(self.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.setPixmap(self.pix)

    def split_rgba(self, rgba):
        r_buf = ImageBuf()
        g_buf = ImageBuf()
        b_buf = ImageBuf()
        a_buf = ImageBuf()
        ImageBufAlgo.channels (r_buf, rgba, ("R",))
        ImageBufAlgo.channels (g_buf, rgba, ("G",))
        ImageBufAlgo.channels (b_buf, rgba, ("B",))
        ImageBufAlgo.channels (a_buf, rgba, ("A",))
        self.img_r, self.img_g, self.img_b, self.img_a = r_buf, g_buf, b_buf, a_buf

class ImageViewModel(ImageModel):
    def __init__(self, text):
        super().__init__()
        self.setText('\n\n {} \n\n'.format(text))
        self.setFixedSize(100,100)

    def set_image(self, rgba):
        pixels = rgba.get_pixels(oiio.UINT8)
        h, w, nchannels = pixels.shape
        if nchannels == 1:
            img = QtGui.QImage(pixels, w, h, w, QtGui.QImage.Format_Grayscale8)
        else:
            img = QtGui.QImage(pixels, w, h, w*3, QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(img)
        self.pix = pix.scaled(self.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.setPixmap(self.pix)


class ImageDropModel(ImageModel):
    def __init__(self):
        super().__init__()
        self.setText('\n\n Drop Image or Click to Browse \n\n')
        self.setFixedSize(250,250)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        if e.mimeData().hasImage:
            e.accept()
        else:
            e.ignore()

    def dragMoveEvent(self, e):
        if e.mimeData().hasImage:
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        if e.mimeData().hasImage:
            e.setDropAction(QtCore.Qt.CopyAction)
            file_path = e.mimeData().urls()[0].toLocalFile()
            for url in e.mimeData().urls():
                filename = url.toLocalFile()
                pixels, spec = open_image_file(filename)
                rgba = ImageBuf(filename)
                current_colorspace = rgba.spec().getattribute('oiio:ColorSpace')
                print(rgba.spec().getattribute('oiio:ColorSpace'))
                if current_colorspace != "sRGB" and current_colorspace != None:
                    rgba = ImageBufAlgo.colorconvert (rgba,str(current_colorspace) , "sRGB")
                self.set_image(rgba)
                self.split_rgba(rgba)
                self.signal.changed.emit()
            e.accept()
        else:
            e.ignore()



'''
    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
            for url in e.mimeData().urls():
                filename = url.toLocalFile()
                self.split_rgba(filename)
                self.openFile(filename)
                self.signal.changed.emit()
        else:
            e.ignore()
'''