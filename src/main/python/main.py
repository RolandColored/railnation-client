from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, QObject
from PyQt5.QtWidgets import QApplication

Form, Window = uic.loadUiType("../dialog.ui")


class App(Form, QObject):
    def setupUi(self, window):
        super().setupUi(window)
        self.btn_prestige.clicked.connect(self.clicked_prestige)

    @pyqtSlot()
    def clicked_prestige(self):
        print('Collecting Prestige information')
        self.btn_loads.setEnabled(False)
        self.btn_storage.setEnabled(False)


if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    form = App()
    form.setupUi(window)
    window.show()
    app.exec()
