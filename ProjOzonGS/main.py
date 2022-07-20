from google_sheets_api import *
from ozon_request import get_parsed_request


if __name__ == '__main__':
    delivering_date_from = '2022-06-01T14:15:22Z'
    delivering_date_to = '2022-07-13T14:15:22Z'

    result = get_parsed_request(delivering_date_from, delivering_date_to)

    api = GoogleSheetsApi(CRED_FILE, SPREADSHEET_ID)
    api.write_header(result['header'])
    api.write_multiple_line(result['data'])
