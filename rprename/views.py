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

    def loadFiles(self):
        self.dstFileList.clear()
        if self.dirEdit.text():
            initDir = self.dirEdit.text()
        else:
            initDir = str(Path.home())
            files, filter_ = QFileDialog.getOpenFileNames(
                self, 'Choose Files to Rename', initDir, filter=FILTERS
            )
            if len(files) > 0:
                fileExtension = filter_[filter_.index('*'): -1]
                self.extensionLabel.setText(fileExtension)
                srcDirName = str(Path(files[0]).parent)
                self.dirEdit.setText(srcDirName)
                for file in files:
                    self._files.append(Path(file))
                    self.srcFileList.addItem(file)
                self._filesCount = len(self._files)
