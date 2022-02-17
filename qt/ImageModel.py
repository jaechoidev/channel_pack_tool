"""
ImageViewModel.py
"""

import sys, os, cv2
import numpy as np
from PySide6 import QtCore, QtWidgets, QtGui
import OpenImageIO as oiio 
import numpy as np
from OpenImageIO import ImageInput, ImageOutput
from OpenImageIO import ImageBuf, ImageSpec, ImageBufAlgo

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
        pixels = input_data.read_image()
        input_data.close()
        return pixels

    def set_image(self, pixels):
        pixels = cv2.normalize(pixels, None, alpha = 0, beta = 255, norm_type = cv2.NORM_MINMAX, dtype = cv2.CV_32F)
        pixels = pixels.astype(np.uint8)
        h, w, _ = pixels.shape
        img = QtGui.QImage(pixels, w, h, 3 * w, QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(img)
        self.pix = pix.scaled(self.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.setPixmap(self.pix)

    def split_rgba(self, pixels):
        n_channels = pixels.shape[2]
        print(n_channels)
        out = {"0": np.zeros(pixels.shape),
                "1": np.zeros(pixels.shape),
                "2": np.zeros(pixels.shape),
                "3": np.zeros(pixels.shape)}
        for i in range(n_channels):
            print(len(out["{}".format(i)][:,:,i]))
            out["{}".format(i)][:,:,i] = pixels[:,:,i]
        self.img_r, self.img_g, self.img_b, self.img_a = out["0"], out["1"], out["2"], out["3"]



class ImageViewModel(ImageModel):
    def __init__(self, text):
        super().__init__()
        self.setText('\n\n {} \n\n'.format(text))
        self.setFixedSize(100,100)


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
                pixels = self.openFile(filename)
                self.set_image(pixels)
                self.split_rgba(pixels)
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