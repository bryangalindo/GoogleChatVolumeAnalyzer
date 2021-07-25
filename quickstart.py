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

def create_google_service(creds, google_product, product_version):
    return build(google_product, product_version, credentials=creds)

def create_values_dict(values):
    return {
        'values': values,
    }

def update_google_sheet(service, body, spreadsheet_id, sheet_range, value_input_option):
    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=sheet_range,
        valueInputOption=value_input_option,
        body=body,).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))

if __name__ == '__main__':
    scopes = [c.READ_WRITE_SCOPE]
    creds = get_auth_creds(c.TOKEN_JSON_FILE, c.CREDENTIALS_JSON_FILE, scopes)
    service = create_google_service(creds, c.GOOGLE_PRODUCT, c.PRODUCT_VERSION)
    values = [
        [
            'Test', 'Test 2', 'Test 3',
        ]
    ]
    body = create_values_dict(values)
    update_google_sheet(service, body, c.SPREADSHEET_ID, c.SHEET_RANGE, c.VALUE_INPUT_OPTION)