from fastmcp import FastMCP
from Services.calendar_service import create_calendar_event,  is_slot_available

from db import save_calendar_event

mcp = FastMCP(name="Calendar MCP Server")


@mcp.tool
def book_appointment(
    title: str,
    start_time: str,
    end_time: str,
    description: str | None = None,
):
    """
    Book an appointment if the time slot is available.
    """
    try: 
        available = is_slot_available(start_time, end_time)
    except Exception as e:
        return {
            "status": "error",
            "stage": "availability_check",
            "message": str(e),
        }
    if not available:
        return {
            "status": "failed",
            "reason": "Time slot is not available",
        }
        
    try:
        event = create_calendar_event(
            title=title,
            start_time=start_time,
            end_time=end_time,
            description=description
        )
    except Exception as e:
        return {
            "status": "error",
            "stage": "calendar_creation",
            "message": str(e),
        }

    google_event_id = event["id"]
    calendar_link = event.get("htmlLink")

    try:
        save_calendar_event(
            title=title,
            start_time=start_time,
            end_time=end_time,
            google_event_id=google_event_id,
            calendar_link=calendar_link,
            description=description
        )

    except Exception as e:
        return {
            "status": "partial_success",
            "message": "Calendar event created but database save failed",
            "google_event_id": google_event_id,
            "calendar_link": calendar_link,
            "db_error": str(e),
        }

    return {
        "status": "success",
        "title": title,
        "google_event_id": google_event_id,
        "calendar_link": calendar_link
    }
    
if __name__ == "__main__":
    mcp.run(transport="http", port=8000)


