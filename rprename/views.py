#!/usr/bin/env python

""" This module provides the RP Rename main window. """
from collections import deque
from pathlib import Path

from PyQt5.QtWidgets import QFileDialog, QWidget
from .ui.window import Ui_Window

FILTERS = ';;'.join(
    (
        'PNG Files (*.png)',
        'JPEG Files (*.jpeg)',
        'JPG Files (*.jpg)',
        'GIF Files (*.gif)',
        'Text Files (*.txt)',
        "Python Files (*.py)",
    )
)


class Window(QWidget, Ui_Window):

    def __init__(self):
        super(Window, self).__init__()
        self._files = deque()
        self._filesCount = len(self._files)
        self._setupUI()

    def _setupUI(self):
        self.setupUi(self)
