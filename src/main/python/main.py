from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QInputDialog, QLineEdit, QWidget

from src.main.python.prestige import association_prestige
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

    @pyqtSlot()
    def clicked_prestige(self):
        print('Collecting Prestige information')
        #self.btn_loads.setEnabled(False)
        #self.btn_storage.setEnabled(False)

        association_prestige(self.api)


if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    form = App()
    form.setupUi(window)
    window.show()
    app.exec()
