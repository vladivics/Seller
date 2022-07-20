from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build

# Constants (must be in .ini file later)
HEADERS_MAX_SIZE = 26

# Google Sheets api info (must be in .ini file too)
CRED_FILE = "credentials.json"
SPREADSHEET_ID = "1Ce8uORJkcBGA3PRIFBKz8HRxYWzLVd_3kWWQABN-Mys"


class GoogleSheetsApi:
    def __init__(self, credential_file, spreadsheet_id):
        self.credential_file = credential_file
        self.spreadsheet_id = spreadsheet_id
        self.last_index = 1

        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self.credential_file,
            ["https://www.googleapis.com/auth/spreadsheets"]
        )
        self.sheets_service = build(
            serviceName="sheets",
            version="v4",
            credentials=credentials
        )

    def __change_single_line(self, index: int, data: list, value_input_option: str):
        body = {
            'values': [
                data
            ]
        }
        body_range = 'A{0}:{1}{0}'.format(index, chr(ord("A") + len(data) - 1))
        self.sheets_service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id,
            valueInputOption=value_input_option,
            range=body_range,
            body=body
        ).execute()

    def delete_single_line(self, index: int):
        if not (1 <= index <= self.last_index):
            raise ValueError('Invalid index (index must be between 1 and {})'.format(self.last_index))

        self.sheets_service.spreadsheets().values().clear(
            spreadsheetId=self.spreadsheet_id,
            range='A{0}:Z{0}'.format(index),
            body={}
        ).execute()
        print(self.last_index)
        print(index)
        if self.last_index == index + 1:
            self.last_index -= 1

    def delete_sheet(self):
        self.sheets_service.spreadsheets().values().clear(
            spreadsheetId=self.spreadsheet_id,
            range='A{0}:Z{1}'.format(1, self.last_index),
            body={}
        ).execute()
        self.last_index = 1

    def write_header(self, header: list, value_input_option='USER_ENTERED'):
        self.__change_single_line(
            index=1,
            data=header,
            value_input_option=value_input_option
        )
        if self.last_index == 1:
            self.last_index += 1

    def write_single_line(self, data: list, value_input_option='USER_ENTERED'):
        if data is None or len(data) == 0:
            raise ValueError('Invalid data (None or empty list)')

        self.__change_single_line(
            index=self.last_index,
            data=data,
            value_input_option=value_input_option
        )
        self.last_index += 1

    def write_multiple_line(self, data: list, value_input_option='USER_ENTERED'):
        for elem in data:
            self.__change_single_line(
                index=self.last_index,
                data=elem,
                value_input_option=value_input_option
            )
            self.last_index += 1
