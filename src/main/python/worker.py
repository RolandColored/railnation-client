import pickle
import traceback

from PyQt5.QtCore import QObject, pyqtSignal
from googleapiclient.discovery import build


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

    def get_gsheet(self, token_file):
        with open(self.token_file, 'rb') as token:
            creds = pickle.load(token)
        service = build('sheets', 'v4', credentials=creds,
                        discoveryServiceUrl='https://sheets.googleapis.com/$discovery/rest?version=v4')
        return service.spreadsheets()
