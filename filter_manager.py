# from __future__ import print_function
import pickle
import os.path
import google_api_helper
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pdb

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = google_api_helper.auth(SCOPES)
    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().settings().filters().list(userId='me').execute()
    filters = results.get('filter', [])

    if not filters:
        print('No filters found.')
    else:
        print('Filters:')
        print(filters)

if __name__ == '__main__':
    main()
