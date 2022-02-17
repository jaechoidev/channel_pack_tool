"""
MainWindow.py
"""

from PySide6 import QtCore, QtWidgets, QtGui
from qt.ImageModel import ImageViewModel, ImageDropModel


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(800, 600)
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
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.image_drop)
        self.preview_layout = QtWidgets.QHBoxLayout()
        self.preview_layout.addWidget(self.image_r)
        self.preview_layout.addWidget(self.image_g)
        self.preview_layout.addWidget(self.image_b)
        self.preview_layout.addWidget(self.image_a)
        self.layout.addLayout(self.preview_layout)
        
    def connections(self):
        self.image_drop.signal.changed.connect(self.set_preview_rgb)
        self.image_drop.signal.clicked.connect(self.test)

    def set_preview_rgb(self):
        self.image_r.set_image(self.image_drop.img_r)
        self.image_g.set_image(self.image_drop.img_g)
        self.image_b.set_image(self.image_drop.img_b)
        self.image_a.set_image(self.image_drop.img_a)

    def test(self):
        print("working!")