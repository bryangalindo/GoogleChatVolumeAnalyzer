import os.path

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


class GoogleCredentials:
    def __init__(self, token_json, credentials_json, scopes):
        self.credentials_json = credentials_json
        self.scopes = scopes
        self.token_json = token_json
        self.credentials = None
                    
    def get_oauth_credentials(self):
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
