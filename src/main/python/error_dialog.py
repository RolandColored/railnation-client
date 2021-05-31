import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel


class ExceptionDialog(QDialog):
    def __init__(self, error: str):
        super().__init__()

        self.setWindowTitle('Unhandled Exception')

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Close)
        self.buttonBox.clicked.connect(self.close_application)

        self.layout = QVBoxLayout()
        message = QLabel(error)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    @pyqtSlot()
    def close_application(self):
        sys.exit(-1)
