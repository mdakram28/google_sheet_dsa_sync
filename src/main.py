import os.path
from time import sleep

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1r4N6f__QzllfPMauWnjtoQ_hRSD1zTMdonXGcdw0ntc'

update = "unknown" # "all", "notaccepted", "unknown"

from leetcode import LeetCode

def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range='B1:E500').execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
        return

    with LeetCode() as leetcode:
        leetcode.login()
        for i, row in enumerate(values):
            if len(row) < 4 or not row[3].lower().startswith(leetcode.problem_url):
                continue
            if update == 'notaccepted' and row[2].lower().strip() == 'accepted':
                continue
            elif update == 'unknown' and row[2].lower().strip():
                continue
            prob_url = row[3]
            prob = leetcode.fetch_problem(prob_url)
            print(prob_url, prob)
            if prob:
                result = service.spreadsheets().values().update(
                    spreadsheetId=SPREADSHEET_ID, range=f"B{i+1}:D{i+1}",
                    valueInputOption="USER_ENTERED", body={ 'values' : [
                        [
                            prob[0]['date'],
                            prob[0]['language'],
                            prob[0]['status'],
                        ]]}).execute()
            else:
                result = service.spreadsheets().values().update(
                    spreadsheetId=SPREADSHEET_ID, range=f"B{i+1}:D{i+1}",
                    valueInputOption="USER_ENTERED", body={ 'values' : [
                        [
                            "",
                            "",
                            "Pending",
                        ]]}).execute()
            sleep(0.3)
        sleep(20)
            
    


if __name__ == '__main__':
    main()