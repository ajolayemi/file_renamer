#!/usr/bin/env python

""" This module provides the RP Rename main window. """
from collections import deque
from pathlib import Path

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QFileDialog, QWidget

from .rename import Renamer
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
        self._connectSignalsSlots()

    def _setupUI(self):
        self.setupUi(self)
        self._updateStateWhenNoFiles()

    def _updateStateWhenNoFiles(self):
        """ This updates the GUI's state when the application is running
        and the list of Files to Rename is empty. """
        self._filesCount = len(self._files)
        self.loadFilesButton.setEnabled(True)
        self.loadFilesButton.setFocus(True)
        self.renameFilesButton.setEnabled(False)
        self.prefixEdit.clear()
        self.prefixEdit.setEnabled(False)

    def _connectSignalsSlots(self):
        self.loadFilesButton.clicked.connect(self.loadFiles)
        self.renameFilesButton.clicked.connect(self.renameFiles)

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
                self._updateStateWhenFilesLoaded()
                fileExtension = filter_[filter_.index('*'): -1]
                self.extensionLabel.setText(fileExtension)
                srcDirName = str(Path(files[0]).parent)
                self.dirEdit.setText(srcDirName)
                for file in files:
                    self._files.append(Path(file))
                    self.srcFileList.addItem(file)
                self._filesCount = len(self._files)

    def _updateStateWhenFilesLoaded(self):
        """ Updates the GUI's state when te lists of Files to Rename contains one or more files. """
        self.prefixEdit.setEnabled(True)
        self.prefixEdit.setFocus(True)

    def renameFiles(self):
        self._runRenamerThread()

    def _runRenamerThread(self):
        prefix = self.prefixEdit.text()
        self._thread = QThread()
        self._renamer = Renamer(
            files=tuple(self._files),
            prefix=prefix
        )
        self._renamer.moveToThread(self._thread)
        # Rename - connecting to renamedFiles signal
        self._thread.started.connect(self._renamer.renameFiles)
        # Update state
        self._renamer.renamedFiles.connect(self._updateStateWhenFileRenamed)
        self._renamer.progressed.connect(self._updateProgressBar)
        self._renamer.finished.connect(self._updateStateWhenNoFiles)
        # Clean up
        self._renamer.finished.connect(self._thread.quit)
        self._renamer.finished.connect(self._renamer.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)

        # Run the thread
        self._thread.start()

    def _updateStateWhenFileRenamed(self, newFile):
        """ When a file is renamed, this method removes the file from the list
        of files to be renamed. It then updates the list of Files to Rename and also the
        list of Renamed Files on the application's GUI. """
        self._files.popleft()
        self.srcFileList.takeItem(0)
        self.dstFileList.addItem(str(newFile))

    def _updateProgressBar(self, fileNumber):
        progressPercent = int(fileNumber / self._filesCount * 100)
        self.progressBar.setValue(progressPercent)