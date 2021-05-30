import pickle
from pprint import pprint
from time import sleep

from googleapiclient.discovery import build

from src.main.python.worker import AbstractWorker


class LoadsWorker(AbstractWorker):
    def __init__(self, api):
        super().__init__(api)

    def run_wrapped(self):
        SPREADSHEET_ID = '1PUkEhDxq59BVvPofj8zucO4NtglX27Wz4m2fiChS_5k'
        SHEET_NAME = 'Endspiel Maindaten'
        FIRST_DATA_ROW = 12
        DONE_COLUMN = 'D'
        IDS_COLUMN = 'Y'
        LEVEL_COLUMN = 'G'
        LOADS_COLUMN = 'I'
        HARBOUR_ID = '01cb7fc7-4321-4762-ae3c-06cb64a896b5'
        WAREHOUSE_ID = '10f808a0-8aba-4e91-9d9f-fe1a3edc1b57'

        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        # get factory IDs
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=f'{SHEET_NAME}!{DONE_COLUMN}{FIRST_DATA_ROW}:{IDS_COLUMN}').execute()
        factories = result.get('values', [])
        print(factories)

        for i, factory in enumerate(factories):
            factory_id = factory[-1]
            done = factory[0]

            if done == 'Ja':
                continue

            if factory_id == WAREHOUSE_ID:
                factory_details = self.api.call('WarehouseInterface', 'getOverview', [factory_id], )['Body']
            elif factory_id == HARBOUR_ID:
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

            sleep(1)
