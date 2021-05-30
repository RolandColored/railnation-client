from PyQt5 import uic
from PyQt5.QtCore import QThread, QObject
from PyQt5.QtWidgets import QApplication, QInputDialog, QLineEdit, QWidget, QFileDialog

from src.main.python.error_dialog import ExceptionDialog
from src.main.python.loads import LoadsWorker
from src.main.python.prestige import PrestigeWorker
from src.main.python.server import ServerCaller

Form, Window = uic.loadUiType("../dialog.ui")


class App(Form, QWidget):
    api = None

    def setupUi(self, window):
        super().setupUi(window)
        self.btn_prestige.clicked.connect(self.clicked_prestige)
        self.btn_loads.clicked.connect(self.clicked_loads)

        server_number, _ = QInputDialog.getInt(self, "Server Number", "Server Number:")
        session_id, _ = QInputDialog.getText(self, "PHPSESSID", "PHPSESSID:", QLineEdit.Normal)
        self.api = ServerCaller(f's{server_number}.railnation.de', session_id)

    def report_progress(self, i, total):
        self.progressBar.setValue(int(i / total * 100))

    def finished_process(self):
        self.report_progress(0, 1)
        self._set_enabled_state_all_buttons(True)

    def handle_exception(self, error: str):
        dlg = ExceptionDialog(error)
        dlg.exec()

    def clicked_prestige(self):
        self._set_enabled_state_all_buttons(False)
        filename = QFileDialog.getSaveFileName(self, 'Datei speichern', "prestige.csv")
        self._process_in_thread(PrestigeWorker(self.api, filename[0]))

    def clicked_loads(self):
        self._set_enabled_state_all_buttons(False)
        self._process_in_thread(LoadsWorker(self.api))

    def _set_enabled_state_all_buttons(self, state: bool):
        buttons = [self.btn_prestige, self.btn_loads, self.btn_storage]
        for button in buttons:
            button.setEnabled(state)

    def _process_in_thread(self, worker_instance: QObject):
        self.thread = QThread()
        self.worker = worker_instance
        self.worker.moveToThread(self.thread)
        # Connect signals and slots
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.progress.connect(self.report_progress)
        self.worker.error.connect(self.handle_exception)

        self.thread.started.connect(self.worker.run)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.finished_process)
        # Start the thread
        self.thread.start()


if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    form = App()
    form.setupUi(window)
    window.show()
    app.exec()
