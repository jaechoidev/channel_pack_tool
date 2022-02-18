"""
ImageViewModel.py
"""

import sys, os, cv2
import numpy as np
from PySide6 import QtCore, QtWidgets, QtGui
import OpenImageIO as oiio 
from OpenImageIO import ImageInput, ImageOutput
from OpenImageIO import ImageBuf, ImageSpec, ImageBufAlgo
from utils.oiio_utils import get_pixmap_from_imgbuf

class Communicate(QtCore.QObject):
    changed = QtCore.Signal()
    clicked = QtCore.Signal()


class ImageModel(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        self.signal = Communicate()
        self.pressed = False
        self.setStyleSheet("QLabel{border: 1px dashed #aaa}")
        self.imgbuf = ImageBuf()

    def mousePressEvent(self, e):
        self.pressed = True

    def mouseReleaseEvent(self, e):
        if self.pressed:
            self.signal.clicked.emit()
            self.pressed = False

    def set_image(self, imgbuf=None):
        imgbuf = imgbuf if imgbuf else self.imgbuf
        pix = get_pixmap_from_imgbuf(imgbuf)
        self.pix = pix.scaled(self.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.setPixmap(self.pix)

    def get_channel(self, channel):
        channel_buf = ImageBuf()
        ImageBufAlgo.channels(channel_buf, self.imgbuf, (channel,))
        return channel_buf


class ImageViewModel(ImageModel):
    def __init__(self, text):
        super().__init__()
        self.setText('\n\n {} \n\n'.format(text))
        self.setFixedSize(100,100)


class ImageDropModel(ImageModel):
    def __init__(self):
        super().__init__()
        self.setText('\n\n Drop Image or Click to Browse \n\n')
        self.setFixedSize(100,100)
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
            self.imgbuf = ImageBuf(file_path)
            self.set_image()
            self.signal.changed.emit()
            e.accept()
        else:
            e.ignore()

