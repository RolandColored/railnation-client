import csv
from time import sleep

from worker import AbstractWorker


class PrestigeWorker(AbstractWorker):
    def __init__(self, api, filename):
        super().__init__(api)
        self.filename = filename

    def run_wrapped(self):
        # association analysis
        assoc_info = self.api.call('CorporationInterface', 'getOtherMemberBuildings',
                                   ["00000000-0000-0000-0000-000000000000"])
        print(f"Info for {len(assoc_info['Body'])} members")

        # fetch all prestige details
        prestiges = {}
        i = 0
        for user_id, member in assoc_info['Body'].items():
            prestiges[user_id] = {}
            prestiges[user_id]['overview'] = self.api.call('BudgetInterface', 'getPrestigeHistoryDetails',
                                                           [user_id, 9])['Body']['balance']
            sleep(1)
            prestiges[user_id]['cities'] = self.api.call('BudgetInterface', 'getPrestigeHistoryDetails',
                                                         [user_id, 9, '0', '1'])['Body']['balance']
            sleep(1)
            prestiges[user_id]['landmarks'] = self.api.call('BudgetInterface', 'getPrestigeHistoryDetails',
                                                            [user_id, 9, '0', '2'])['Body']['balance']
            sleep(2)
            i += 1
            self.progress.emit(i, len(assoc_info['Body']))

        # fetch all profiles for the nick names
        user_ids = list(prestiges.keys())
        profiles = self.api.call('ProfileInterface', 'getVCard', [user_ids], short_call=1236)['Body']

        # prepare all city and landmarks for the csv header line
        cities = set(city['type'] for user_id, prestige in prestiges.items() for city in prestige['cities'])
        landmarks = set(landmark['type'] for user_id, prestige in prestiges.items() for landmark in prestige['landmarks'])

        with open(self.filename, 'w', newline='') as csvfile:
            fieldnames = ['member', 'transports', 'invests', 'trainstation', 'other', 'competition', 'medal',
                          '-cities-'] + list(cities) + ['-landmarks-'] + list(landmarks)
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for user_id, prestige in prestiges.items():
                overview_dict = {
                    'transports': [row for row in prestige['overview'] if row['type'] == '0'],
                    'invests': [row for row in prestige['overview'] if row['type'] == '3'],
                    'trainstation': [row for row in prestige['overview'] if row['type'] == '4'],
                    'other': [row for row in prestige['overview'] if row['type'] == '6'],
                    'competition': [row for row in prestige['overview'] if row['type'] == '7'],
                    'medal': [row for row in prestige['overview'] if row['type'] == '8'],
                }
                write_dict = {'member': profiles[user_id]['userName']}
                for key, value in overview_dict.items():
                    if len(value) > 0:
                        write_dict[key] = value[0]['prestige']

                for row in prestige['cities']:
                    write_dict[row['type']] = row['prestige']
                for row in prestige['landmarks']:
                    write_dict[row['type']] = row['prestige']

                writer.writerow(write_dict)
        self.finished.emit()
