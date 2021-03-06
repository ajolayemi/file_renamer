""" This module provides Renamer class to rename multiple files. """

import time
from pathlib import Path

from PyQt5.QtCore import QObject, pyqtSignal


class Renamer(QObject):
    # Custom signals
    progressed = pyqtSignal(int)
    renamedFiles = pyqtSignal(Path)
    finished = pyqtSignal()

    def __init__(self, files, prefix):
        super(Renamer, self).__init__()
        self._files = files
        self._prefix = prefix

    def renameFiles(self):
        for fileNumber, file in enumerate(self._files, 1):
            newFile = file.parent.joinpath(
                f'{self._prefix}{str(fileNumber)}{file.suffix}'
            )
            file.rename(newFile)
            time.sleep(0.1)  # This slows down the renaming process
            self.progressed.emit(fileNumber)
            self.renamedFiles.emit(newFile)
        self.progressed.emit(0)
        self.finished.emit()
