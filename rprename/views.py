#!/usr/bin/env python

""" This module provides the RP Rename main window. """
from collections import deque
from pathlib import Path

from PyQt5.QtWidgets import QFileDialog, QWidget
from .ui.window import Ui_Window


class Window(QWidget, Ui_Window):

    def __init__(self):
        super(Window, self).__init__()
        self._setupUI()

    def _setupUI(self):
        self.setupUi(self)
