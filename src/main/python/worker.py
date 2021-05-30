import sys
import traceback

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel


class AbstractWorker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int, int)
    error = pyqtSignal(str)

    def __init__(self, api):
        super().__init__()
        self.api = api

    def run(self):
        try:
            self.run_wrapped()
        except:
            self.error.emit(traceback.format_exc())

    def run_wrapped(self):
        raise NotImplementedError()

