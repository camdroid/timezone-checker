from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import usaddress
import us
import pdb

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = (datetime.datetime.utcnow() - datetime.timedelta(days=1)).isoformat() + 'Z' # 'Z' indicates UTC time
    timeMax = (datetime.datetime.utcnow() + datetime.timedelta(days=28)).isoformat()+'Z'
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime', timeMax=timeMax).execute()
    events = events_result.get('items', [])

    def get_time_zones_for_event(event):
        time_zones = []
        if 'location' not in event:
            print('No location found for event')
            return None
        location = usaddress.parse(event['location'])
        state_tuple = [l for l in location if 'StateName' in l]
        if state_tuple:
            state_code = [c for c in state_tuple[0] if c is not 'StateName'][0]
            state = us.states.lookup(state_code)
            if state:
                time_zones = state.time_zones

        print('Potential time_zones: ', time_zones)
        return time_zones

    def event_name(event):
        name = event.get('summary')
        if not name:
            return 'No title found'
        return name.split('\n')[0]

    if not events:
        print('No upcoming events found.')
    events = [events[2]]
    for event in events:
        print('Looking at event: ', event_name(event))
        time_zones = get_time_zones_for_event(event)
        if event['start'].get('timeZone') is None:
            print('This event has no time zone')
        elif event['start'].get('timeZone') in time_zones:
            print('Time zone matches location!')
        elif event['start'].get('timeZone') not in time_zones:
            pdb.set_trace()
            print('Careful! This event may not be in the right timezone!')
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
        else:
            print('How did you get here?')

if __name__ == '__main__':
    main()
