#!/usr/bin/env python

""" This module provides the RP Rename application. """
import sys
from PyQt5.QtWidgets import QApplication
from .views import Window


def main():
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())