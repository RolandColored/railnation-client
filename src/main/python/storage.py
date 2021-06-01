from datetime import datetime
from time import sleep

from config import *
from worker import AbstractWorker


class StorageWorker(AbstractWorker):
    def __init__(self, api, token_file):
        super().__init__(api)
        self.token_file = token_file

    def _active_town_id(self, sheet):
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=ACTIVE_TOWN).execute()
        town_name = result.get('values', [])[0][0]
        print(town_name)
        return TOWN_MAPPING[town_name]

    def run_wrapped(self):
        sheet = self.get_gsheet(self.token_file)
        town_id = self._active_town_id(sheet)

        while True:
            # refresh based on total runtime
            result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=TOTAL_TRIP).execute()
            try:
                refresh_interval = int(result.get('values', [])[0][0].replace('s', ''))
            except ValueError:
                refresh_interval = 60
            refresh_interval = min(refresh_interval, 300)  # avoid extreme waiting times

            # current good
            result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=CURRENT_GOOD).execute()
            try:
                current_good = int(result.get('values', [])[0][0])
            except ValueError:
                current_good = None

            # get town data
            town_details = self.api.call('LocationInterface', 'getTownDetails', [town_id], )['Body']

            delivered = 0
            if current_good is not None:
                deliveries = self.api.call('EndgameInterface', 'getTransportListCorporation', [town_id, current_good, 20, 0], )['Body']
                if len(deliveries) > 0:
                    delivered = sum(corp_deliveries['Delivered'] for corp, corp_deliveries in deliveries['Corporation'].items())

            # update storages
            result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=STORAGES_RANGE).execute()
            last_values = result.get('values', [])

            values = []
            for i, resource in enumerate(town_details['StoragesInfo']['Storages']):
                # fill row with town storage values
                row = [resource['ResourceId'], resource['Limit'], resource['ConsumptionAmount'], resource['Amount'],
                       last_values[i][3] if len(last_values[i]) > 3 else '']

                # new block - remove old values
                if resource['ResourceId'] != int(last_values[i][0]):
                    row += [''] * 45

                # fill row with historic delivered values for overall delivery performance
                elif current_good is not None and resource['ResourceId'] == current_good:
                    row += [delivered] + last_values[i][5:50]
                values.append(row)

            sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=STORAGES_RANGE,
                                  valueInputOption='USER_ENTERED', body={'values': values}).execute()

            # refresh last update
            values = [[datetime.now().strftime("%H:%M:%S")]]
            sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=UPDATE_CELL,
                                  valueInputOption='USER_ENTERED', body={'values': values}).execute()

            for i in range(refresh_interval):
                sleep(1)
                self.progress.emit(i, refresh_interval)
