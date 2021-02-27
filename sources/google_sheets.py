import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def auth():
    """Shows basic usage of the Sheets API.
    """
    # If modifying these scopes, delete the file token.pickle.
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    creds = None
    pickle_path = os.path.expanduser('secrets/token.pickle')
    cred_path = os.path.expanduser('secrets/google_credentials.json')

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(pickle_path):
        with open(pickle_path, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(cred_path, scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(pickle_path, 'wb') as token:
            pickle.dump(creds, token)

    return build('sheets', 'v4', credentials=creds, cache_discovery=False)


def create_sheet(service, title):
    sheet = {'properties': {'title': title}}
    sheet = service.spreadsheets().create(body=sheet,
                                          fields='spreadsheetId').execute()
    return sheet.get('spreadsheetId')


def write_df(service, sheet_id, sheet_range, df):
    data = {'values': [df.columns.values.tolist()] + df.values.tolist()}
    return service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        valueInputOption='USER_ENTERED',
        range=sheet_range,
        body=data
    ).execute()
