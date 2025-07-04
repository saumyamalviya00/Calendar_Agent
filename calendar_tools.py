import json
from google_apis import create_service


client_secret = 'client_secret.json'

def construct_google_calendar_client(client_secret):

    """
    construct a google calendar API client.
    
    Parsmeters :
    -client_secret (str): The path to the client JSON file.
    
    Returns:
    -service: The google Calendar API service instance.
    """
    API_NAME = 'calendar'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    service = create_service(client_secret,API_NAME ,API_VERSION , SCOPES)
    return service

calendar_service = construct_google_calendar_client(client_secret)

def create_calendar(calendar_name):
    """
    creates a new calendar list.
    
    Parameters:
    -calendar_name(str): the name of the newcalendar list.
    
    Returns:
    -dict: A dictionary containing the ID of the new calendar list.
    """
    calendar_list = {
        'summary' : calendar_name
    }
    created_calendar_list = calendar_service.calendars().insert(body=calendar_list).execute()
    return created_calendar_list

def list_calendar_list(max_capacity=200):
    """
    Lists calendar lists until the total number of items reaches max_capacity.
    
    Parameters:
    -max_capacity(int or str, optional): The maximum number of calendar lists to retrieve. Default to 200.
      If a string is provided, it will be converted to an integer.
    
    Returns:
    -list: A list of dictionaries containing cleaned calendar list information with 'id', 'name', and 'description'.
    """
    if isinstance(max_capacity, str):
        max_capacity = int(max_capacity)
        
    all_calendars = []
    all_calendars_cleaned = []
    next_page_token = None
    capacity_tracker = 0
    
    while True:    
        calendar_list = calendar_service.calendarList().list(
            maxResults = min(200, max_capacity - capacity_tracker),
            pageToken = next_page_token
        ).execute()
        calendars= calendar_list.get('items', [])
        all_calendars.extend(calendars)
        capacity_tracker += len(calendars)
        if capacity_tracker >= max_capacity:
           break
        next_page_token = calendar_list.get('nextPageToken')
        if not next_page_token:
            break
        
    for calendar in all_calendars: 
        all_calendars_cleaned.append(
            {
                'id': calendar['id'],
                'name': calendar['summary'],
                'description': calendar.get('description', '')
            })
    return all_calendars_cleaned

def list_calendar_events(calendar_id, max_capacity =20):
    """
    Lists events from a specific calendar until the total number of items reaches max_capacity.
    
    Parameters:
    -calendar_id (str): The ID of the calendar from which to list events.
    -max_capacity (int or str, optional): The maximum number of events to retrieve. Defaults to 20.
      If a string is provided, it will be converted to an integer.
      
    Returns:
    -List: A list of events from the specified calendar.
    """
    
    if isinstance(max_capacity, str):
        max_capacity = int(max_capacity)
        
    all_events = []
    next_page_token = None
    capacity_tracker = 0
    while True:
        events = calendar_service.events().list(
            calendarId=calendar_id,
            maxResults=min(200, max_capacity - capacity_tracker),
            pageToken=next_page_token
        ).execute()
        events = events.get('items', [])
        all_events.extend(events)
        capacity_tracker += len(events)
        if capacity_tracker >= max_capacity:
            break
        next_page_token = events.get('nextPageToken')
        if not next_page_token:
            break
    return all_events

def insert_calendar_event(calendar_id, **kwargs):
    """
    Inser an event into a specific calendar.
    Parameters:
    -service: The Google Calendar API service instance.
    -calendar_id: the ID of the calendar where the event will be inserted.
    -**kwargs: Additional keyword arguments representing the event details.
    Returns:
    - the created event. 
    """
    request_body = json.loads(kwargs['kwargs'])
    event = calendar_service.events().insert(
        calendarId = calendar_id,
        body=request_body
    ).execute() 
    return event
