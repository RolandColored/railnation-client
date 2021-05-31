import sys

from PyQt5 import uic
from PyQt5.QtCore import QThread, QObject
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QFileDialog, QDialog
from fbs_runtime.application_context.PyQt5 import ApplicationContext

from error_dialog import ExceptionDialog
from loads import LoadsWorker
from prestige import PrestigeWorker
from server import ServerCaller
from storage import StorageWorker


class App(QDialog):
    api = None

    def __init__(self, ui, parent=None):
        super().__init__(parent)
        uic.loadUi(ui, self)

        self.btn_prestige.clicked.connect(self.clicked_prestige)
        self.btn_loads.clicked.connect(self.clicked_loads)
        self.btn_storage.clicked.connect(self.clicked_storage)

        server_number, _ = QInputDialog.getInt(self, "Server Nummer", "s???")
        session_id, _ = QInputDialog.getText(self, "Session ID", "PHPSESSID:", QLineEdit.Normal)
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
        filename = QFileDialog.getSaveFileName(self, 'Datei speichern', 'prestige.csv')
        self._process_in_thread(PrestigeWorker(self.api, filename[0]))

    def clicked_loads(self):
        self._set_enabled_state_all_buttons(False)
        filename = QFileDialog.getOpenFileName(self, 'token.pickle')
        self._process_in_thread(LoadsWorker(self.api, filename[0]))

    def clicked_storage(self):
        self._set_enabled_state_all_buttons(False)
        filename = QFileDialog.getOpenFileName(self, 'token.pickle')
        self._process_in_thread(StorageWorker(self.api, filename[0]))

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
    appctxt = ApplicationContext()  # 1. Instantiate ApplicationContext
    dialog = appctxt.get_resource('dialog.ui')
    window = App(dialog)
    window.show()
    exit_code = appctxt.app.exec()  # 2. Invoke appctxt.app.exec()
    sys.exit(exit_code)
