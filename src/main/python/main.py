import traceback

from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, QThread
from PyQt5.QtWidgets import QApplication, QInputDialog, QLineEdit, QWidget, QDialog, QDialogButtonBox, \
    QVBoxLayout, QLabel, QFileDialog

from src.main.python.prestige import PrestigeWorker
from src.main.python.server import ServerCaller

Form, Window = uic.loadUiType("../dialog.ui")


class App(Form, QWidget):
    api = None

    def setupUi(self, window):
        super().setupUi(window)
        self.btn_prestige.clicked.connect(self.clicked_prestige)

        server_number, _ = QInputDialog.getInt(self, "Server Number", "Server Number:")
        session_id, _ = QInputDialog.getText(self, "PHPSESSID", "PHPSESSID:", QLineEdit.Normal)
        self.api = ServerCaller(f's{server_number}.railnation.de', session_id)

    def report_progress(self, i, total):
        self.progressBar.setValue(int(i / total * 100))

    def finished_process(self):
        print('Cleanup')
        self.report_progress(0, 1)
        self.btn_prestige.setEnabled(True)
        self.btn_loads.setEnabled(True)
        self.btn_storage.setEnabled(True)

    def clicked_prestige(self):
        self.btn_prestige.setEnabled(False)
        self.btn_loads.setEnabled(False)
        self.btn_storage.setEnabled(False)
        filename = QFileDialog.getSaveFileName(self, 'Datei speichern', "prestige.csv")

        try:
            self.thread = QThread()
            self.worker = PrestigeWorker(self.api, filename[0])
            self.worker.moveToThread(self.thread)
            # Step 5: Connect signals and slots
            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.progress.connect(self.report_progress)
            self.thread.finished.connect(self.finished_process)
            # Step 6: Start the thread
            self.thread.start()
        except:
            dlg = ExceptionDialog()
            dlg.exec()


class ExceptionDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Unhandled Exception')

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Close)
        self.buttonBox.clicked.connect(self.close_application)

        self.layout = QVBoxLayout()
        message = QLabel(traceback.format_exc())
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    @pyqtSlot()
    def close_application(self):
        exit(-1)


if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    form = App()
    form.setupUi(window)
    window.show()
    app.exec()
