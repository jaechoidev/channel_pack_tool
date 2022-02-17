"""
App.py

$ pyinstaller App.py \
--paths="/Users/jaeyoungchoi/workspace/channel_pack_tool" \
--onefile \
--noconsole

"""

import sys
from PySide6 import QtCore, QtWidgets, QtGui
from qt.MainWindow import MainWindow


class App(QtWidgets.QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.MainWindow = MainWindow()
        self.MainWindow.show()
        

if __name__ == "__main__":
    app = App(sys.argv)
    sys.exit(app.exec())
