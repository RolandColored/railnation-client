SPREADSHEET_ID = '1PUkEhDxq59BVvPofj8zucO4NtglX27Wz4m2fiChS_5k'
SHEET_NAME = 'Endspiel Maindaten'

# loads refresh
FIRST_DATA_ROW = 12
DONE_COLUMN = 'D'
IDS_COLUMN = 'Y'
LEVEL_COLUMN = 'G'
LOADS_COLUMN = 'I'

# town storage
ACTIVE_TOWN = f'{SHEET_NAME}!K3'
STORAGES_RANGE = 'Stadtlager Liveintervalle!C2:BZ'
TOTAL_TRIP = f'{SHEET_NAME}!O4'
UPDATE_CELL = f'{SHEET_NAME}!O7'
CURRENT_GOOD = f'{SHEET_NAME}!Y7'

TOWN_MAPPING = {'Malaga': '0fda8cca-54e2-40c1-bf18-7722ebc1c878', 'Lissabon': '719e411a-ada8-4fa9-a5d4-afc34c4450bb',
                'Porto': '51948fe2-6ffb-4062-ae44-fb270056a733', 'Madrid': '222f192e-4fb8-4a61-b6e4-50083b5dcd51',
                'Barcelona': '3bf8e837-3c71-4756-8c98-95419c132158',
                'Marseille': 'aa9c37dc-eaa1-4cd4-81a3-e01cf993e3a4', 'Bordeaux': 'ea34d204-9228-4f65-b81c-aa2b8eb0acfe',
                'Lyon': '0d180354-ca7c-4d10-ab5a-0277bfee089d', 'Paris': '3e932a82-9f7c-43f1-9f55-263318695c5b',
                'Brüssel': 'fe83c9f6-1de0-4878-9df8-8b84a8104e04', 'London': 'd7a33a63-4e01-406e-86cb-7a91439d976c',
                'Cardiff': 'd98b7f24-e9d7-4037-b6b9-d59847dca1b4', 'Manchester': 'ce440511-3b34-485b-8b0a-85976571d225',
                'Glasgow': 'a18dcd53-7ab5-422e-b56c-e1c1c9e19782', 'Dublin': '8ea40c18-93c5-45a0-a484-117dd737b148',
                'Köln': '6e008baf-c1bf-4bdc-aa69-4fec7fe74727', 'Amsterdam': 'd8e23462-a399-4720-99aa-cccedec13ea7',
                'Hamburg': 'eb0e96fb-01d2-41f7-911a-d23caa56fc02', 'Berlin': '4c317fd3-c6af-4b6c-b77c-fd868856cacf',
                'München': '8f3bf053-e0ba-40cb-98c2-22e717746cfe', 'Zürich': 'bccccd16-b679-4b52-802c-cd4a7095dac3',
                'Prag': '3d64a671-65c3-4ce3-aadf-040a921ed894', 'Mailand': '3f15210f-f801-43dd-afb5-fb05a64613d6',
                'Rom': '95b3a3af-4cb6-4f2c-9188-b128ab9e01a2', 'Neapel': 'dbb903fa-9af0-4ef1-aa57-8f9c7f1c90ec',
                'Palermo': '736b0a16-cf1a-4ca1-9a10-ef874a87e680', 'Kopenhagen': '9ad75ca5-62ed-475d-b969-be51eb154ad5',
                'Göteborg': 'f8c4ad26-1fcc-4b03-b2d4-122f5207f120', 'Oslo': 'bf78bf7e-a797-48d7-9a20-26db492537dc',
                'Stockholm': '4b9dc9f1-ff1b-4982-b666-f628188ddfe3', 'Helsinki': '67a3d545-0769-4ac5-91f2-85fe49e16216',
                'St.Petersburg': 'b26c5d28-0b88-406e-ae68-ebda130c7874',
                'Moskau': 'c7857d84-d736-4326-8cf3-0991ec7e6bb1', 'Minsk': 'c891698b-abef-44e6-ac7c-d4dcd2032cdd',
                'Kiew': 'd3b43a44-7590-472b-a2a4-1da4d763c404', 'Donezk': 'e18d3566-c7db-4bf0-a668-2ed5f0267e31',
                'Riga': '794ded4a-011f-4dbb-ae66-78335e37cdd2', 'Vilnius': '06c145d4-f91e-4138-b282-759f70fa9e11',
                'Danzig': '31165394-09e0-4b7c-a05a-6dfb072dd5e8', 'Warschau': '72911937-210c-4b89-aab0-78968daf0284',
                'Chisinau': '2db3d628-b313-4418-8869-5f9a42234676', 'Bukarest': 'dc9f20a3-2264-44fa-a2c8-9741a0584b94',
                'Istanbul': 'b9dced0b-c3f0-4520-9bee-2b3aac41ee3e', 'Sofia': '34409c74-259b-4cf7-a29b-abd2ec24e7db',
                'Athen': 'd390b017-b40b-4f54-a26e-e2a523ea238c', 'Belgrad': '35acc709-64b3-4322-9faa-657dd9bcbdf1',
                'Sarajevo': 'b05a482b-ac2b-4842-af42-4274dfc392cf', 'Zagreb': 'ec993ec5-0fe0-4f49-9eec-0ecb7bfa0d43',
                'Budapest': 'ff1e890b-d663-41da-952c-46b6612d83c0', 'Wien': '6c21a3da-c436-48ee-bfc6-912e97cc68f9'}
