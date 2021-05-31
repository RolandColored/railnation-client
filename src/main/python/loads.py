import pickle
from pprint import pprint
from time import sleep

from googleapiclient.discovery import build

from config import *
from worker import AbstractWorker


class LoadsWorker(AbstractWorker):
    def __init__(self, api, token_file):
        super().__init__(api)
        self.token_file = token_file

    def run_wrapped(self):
        with open(self.token_file, 'rb') as token:
            creds = pickle.load(token)
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        # get factory IDs
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=f'{SHEET_NAME}!{DONE_COLUMN}{FIRST_DATA_ROW}:{IDS_COLUMN}').execute()
        factories = result.get('values', [])

        for i, factory in enumerate(factories):
            if len(factory) < 10:
                continue  # invalid row

            factory_id = factory[-1]
            good_done = factory[0]
            factory_name = factory[2]

            if good_done == 'Ja':
                continue

            if 'Lager' in factory_name:
                factory_details = self.api.call('WarehouseInterface', 'getOverview', [factory_id], )['Body']
            elif 'Hafen' in factory_name:
                factory_details = self.api.call('HarborInterface', 'getOverview', [factory_id], )['Body']
            else:
                factory_details = self.api.call('LocationInterface', 'getFactoryDetails', [factory_id], )['Body']

            result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                        range=f'{SHEET_NAME}!{LEVEL_COLUMN}{FIRST_DATA_ROW+i}:{LOADS_COLUMN}{FIRST_DATA_ROW+i}').execute()
            values = result.get('values', [])
            try:
                values[0][0] = factory_details['Level']
                values[0][2] = factory_details['WorkloadInfo']['Workload'] if 'WorkloadInfo' in factory_details else factory_details['WorkLoadInfo']['Workload']
                sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=f'{SHEET_NAME}!{LEVEL_COLUMN}{FIRST_DATA_ROW+i}:{LOADS_COLUMN}{FIRST_DATA_ROW+i}',
                                      valueInputOption='USER_ENTERED', body={'values': values}).execute()
            except KeyError as err:
                print(err)
                print(i, factory_id)
                pprint(factory_details)

            self.progress.emit(i, len(factories))
            sleep(1)
        self.finished.emit()
