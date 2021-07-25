from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import constants as c

# If modifying these scopes, delete the file token.json.
SCOPES = [c.READ_WRITE_SCOPE]

def get_auth_creds(token_json, credentials_json, scopes):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_json):
        creds = Credentials.from_authorized_user_file(token_json, scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_json, scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_json, 'w') as token:
            token.write(creds.to_json())
            
    return creds

def create_google_service(google_product, product_version):
    creds = get_auth_creds()
    return build(google_product, product_version, credentials=creds)

def create_append_body(values):
    return {
        'values': values,
    }

def update_google_sheet(service, values, spreadsheet_id, sheet_range, value_input_option):
    body = create_append_body(values)
    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=sheet_range,
        valueInputOption=value_input_option,
        body=body,).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))

def main():
    """
    Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(c.TOKEN_JSON_FILE):
        creds = Credentials.from_authorized_user_file(c.TOKEN_JSON_FILE, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(c.CREDENTIALS_JSON_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(c.TOKEN_JSON_FILE, 'w') as token:
            token.write(creds.to_json())

    service = build(c.GOOGLE_PRODUCT, c.VERSION, credentials=creds)

    # Call the Sheets API
    values = [
        [
        'Test 3', 'Test 4', 'Test 7', 'TEST', 'TESTFDCC', 'testSXSS', None
        ],
    ]
    body = {
        'values': values
    }
    result = service.spreadsheets().values().append(
        spreadsheetId=c.SPREADSHEET_ID,
        range=c.SHEET_RANGE,
        valueInputOption=c.VALUE_INPUT_OPTION,
        body=body,).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))

if __name__ == '__main__':
    pass