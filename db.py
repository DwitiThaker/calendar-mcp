from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

supabase=create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_API_KEY")
)

def save_calendar_event(
        title: str,
        start_time: str,
        end_time: str,
        google_event_id: str,
        calendar_link: str | None = None,
        description: str | None = None

):
    response = supabase.table("calendar_events").insert({
        "title": title,
        "description": description,
        "start_time": start_time,
        "end_time": end_time,
        "google_event_id": google_event_id,
        "calendar_link": calendar_link,
    }).execute().data

    return response
