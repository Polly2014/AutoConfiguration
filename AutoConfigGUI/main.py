# -*- coding: utf-8 -*-


from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

from IndexWindow import IndexWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = IndexWindow()
    window.show()
    sys.exit(app.exec_())
