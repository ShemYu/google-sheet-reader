from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


class GoogleSheets:
    def __init__(self, sheet_id, sheet_name, range):
        self.spreadsheet_id = sheet_id
        self.range_name = "{}!{}".format(sheet_name, range)
        self._scope = ['https://www.googleapis.com/auth/spreadsheets']
        self._get_credentials()
        self._new_service()

    def _get_credentials(self):
        self.creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', self._scope)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'docs/credentials.json', self._scope)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('docs/token.json', 'w') as token:
                token.write(self.creds.to_json())
    
    def _new_service(self):
        self.service =build('sheets', 'v4', credentials=self.creds)
    
    def load(self):
        # Call the Sheets API
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.spreadsheet_id,
                                    range=self.range_name).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
        else:
            print('Name, Major:')
            for row in values:
                # Print columns A and E, which correspond to indices 0 and 4.
                print('%s, %s' % (row[0], row[4]))
