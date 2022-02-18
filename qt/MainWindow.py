"""
MainWindow.py
"""

from PySide6 import QtCore, QtWidgets, QtGui
from qt.ImageModel import ImageViewModel, ImageDropModel


class ImageView(QtWidgets.QWidget):
    def __init__(self):
        super(ImageView, self).__init__()
        self.widgets()
        self.layouts()
        self.connections()

    def widgets(self):
        self.image_drop = ImageDropModel()
        self.image_r = ImageViewModel("r")
        self.image_g = ImageViewModel("g")
        self.image_b = ImageViewModel("b")
        self.image_a = ImageViewModel("a")

    def layouts(self):
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.image_drop)
        self.layout.addWidget(self.image_r)
        self.layout.addWidget(self.image_g)
        self.layout.addWidget(self.image_b)
        self.layout.addWidget(self.image_a)

    def connections(self):
        self.image_drop.signal.changed.connect(self.set_preview_rgb)
        self.image_drop.signal.clicked.connect(self.test)

    def set_preview_rgb(self):
        self.image_r.set_image(self.image_drop.get_channel("R"))
        self.image_g.set_image(self.image_drop.get_channel("G"))
        self.image_b.set_image(self.image_drop.get_channel("B"))
        self.image_a.set_image(self.image_drop.get_channel("A"))

    def test(self):
        print("working!")



class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(800, 600)
        self.widgets()
        self.layouts()

    def widgets(self):
        self.image_01 = ImageView()
        self.image_02 = ImageView()
        self.image_03 = ImageView()
        self.image_04 = ImageView()

    def layouts(self):
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.image_01)
        self.layout.addWidget(self.image_02)
        self.layout.addWidget(self.image_03)
        self.layout.addWidget(self.image_04)

        
