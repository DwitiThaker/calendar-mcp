from googleapiclient.discovery import build
from Services.calendar_auth import get_credentials

def get_calendar_service():
    creds = get_credentials()
    return build("calendar", "v3", credentials=creds)

def create_calendar_event(
    title: str,
    start_time: str,
    end_time: str,
    description: str | None = None,
):
    event = {
        "summary": title,
        "description": description,
        "start": {
            "dateTime": start_time,
            "timeZone": "Asia/Kolkata",
        },
        "end": {
            "dateTime": end_time,
            "timeZone": "Asia/Kolkata",
        }
    }
    service = get_calendar_service()


    created_event = service.events().insert(
        calendarId="primary",
        body=event
    ).execute()
    return created_event



def is_slot_available(start_time :str, end_time: str):
    """
    Check if the primary calendar is free between start_time and end_time.
    """

    service = get_calendar_service()

    body = {
        "timeMin": start_time,
        "timeMax": end_time,
        "timeZone": "Asia/Kolkata",
        "items": [
            {"id": "primary"}
        ]        
    }

    response = service.freebusy().query(body=body).execute()
    busy_slots = response["calendars"]["primary"]["busy"]
    return len(busy_slots) == 0

