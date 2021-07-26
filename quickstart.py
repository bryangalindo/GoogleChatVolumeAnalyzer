import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import constants as c      
import helpers as h


class GoogleCredentials:
    def __init__(self, token_json, credentials_json, scopes):
        self.credentials_json = credentials_json
        self.scopes = scopes
        self.token_json = token_json
        self.credentials = None
                    
    def get_credentials(self):
        token_exists = self.__token_exists()
        if token_exists:
            self.credentials = Credentials.from_authorized_user_file(self.token_json, self.scopes)
        token_invalid = self.__token_invalid()
        if token_invalid:
            token_expired = self.__token_expired()
            if token_expired:
                self.credentials.refresh(Request())
            else:
                self.credentials = self.__get_credentials_from_redirect()
                print(self.credentials)
            self.__create_token_json_file()
        return self.credentials
    
    def __create_token_json_file(self):
        with open(self.token_json, 'w') as token:
            token.write(self.credentials.to_json())
    
    def __get_credentials_from_redirect(self):
        flow = InstalledAppFlow.from_client_secrets_file(self.credentials_json, self.scopes)
        return flow.run_local_server(port=0)
    
    def __token_exists(self):
        if os.path.exists(self.token_json):
            return True
    
    def __token_expired(self):
        if self.credentials and self.credentials.expired and self.credentials.refresh_token:
            return True
        
    def __token_invalid(self):
        if not self.credentials or not self.credentials.valid:
            return True
        
def create_google_service(creds, google_product, product_version):
    return build(google_product, product_version, credentials=creds)

def update_google_sheet(service, body, spreadsheet_id, sheet_range, value_input_option):
    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=sheet_range,
        valueInputOption=value_input_option,
        body=body,).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))

if __name__ == '__main__':
    scopes = [c.READ_WRITE_SCOPE]
    creds_object = GoogleCredentials(c.TOKEN_JSON_FILE, c.CREDENTIALS_JSON_FILE, scopes)
    creds = creds_object.get_credentials()
    service = create_google_service(creds, c.GOOGLE_PRODUCT, c.PRODUCT_VERSION)
    values = [
        [
            'Test', 'Test 2', 'Test 7',
        ]
    ]
    body = h.create_values_dict(values)
    update_google_sheet(service, body, c.SPREADSHEET_ID, c.SHEET_RANGE, c.VALUE_INPUT_OPTION)