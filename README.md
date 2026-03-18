# 📅 calendar-mcp

A Python-based **MCP (Model Context Protocol) (FastMCP) server** that connects Google Calendar with a Supabase database — enabling AI agents to check availability and book appointments through standardized MCP tools.

---

## Architecture

```
Client → Proxy Server (port 9000) → MCP Server (port 8000)
                                            ↓              ↓
                                    Google Calendar    Supabase DB
```

The project follows a clean layered design:

- **MCP Server** (`server.py`) — exposes tools via FastMCP over HTTP
- **Service Layer** (`Services/calendar_service.py`) — wraps the Google Calendar API
- **Database Layer** (`db.py`) — persists events to Supabase
- **Proxy Server** (`proxy_server.py`) — optional intermediary for forwarding requests

---

## Features

- ✅ Check if a time slot is available on Google Calendar
- ✅ Book an appointment (checks availability → creates event → saves to DB)
- ✅ Graceful error handling with distinct status codes (`success`, `failed`, `error`, `partial_success`)
- ✅ Proxy server for extensibility (auth, rate limiting, etc.)

---

## Prerequisites

- Python 3.10+
- A Google Cloud project with the **Google Calendar API** enabled
- OAuth 2.0 credentials (downloaded as `credentials.json`)
- A [Supabase](https://supabase.com/) project with a `calendar_events` table

---

## Installation

```bash
git clone https://github.com/DwitiThaker/calendar-mcp.git
cd calendar-mcp
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_API_KEY=your_supabase_anon_or_service_key
```

> Also ensure `python-dotenv` is installed: `pip install python-dotenv`

---

## Supabase Table Schema

Create a `calendar_events` table in your Supabase project with the following columns:

| Column | Type |
|---|---|
| `id` | uuid (primary key) |
| `title` | text |
| `description` | text (nullable) |
| `start_time` | text |
| `end_time` | text |
| `google_event_id` | text |
| `calendar_link` | text (nullable) |

---

## Running the Server

### Start the MCP Server (port 8000)

```bash
python server.py
```

### (Optional) Start the Proxy Server (port 9000)

```bash
python proxy_server.py
```

The proxy forwards requests from `http://127.0.0.1:9000` to the MCP server at `http://127.0.0.1:8000`.

---

## MCP Tools

### `check_availability`

Check if a time slot is free on Google Calendar.

**Parameters:**

| Name | Type | Description |
|---|---|---|
| `start_time` | `str` | Start of the time slot (ISO 8601, e.g. `2025-06-01T10:00:00`) |
| `end_time` | `str` | End of the time slot (ISO 8601) |

**Response:**
```json
{ "status": "success", "available": true }
```

---

### `book_appointment`

Book an appointment if the requested slot is available.

**Parameters:**

| Name | Type | Description |
|---|---|---|
| `title` | `str` | Title of the event |
| `start_time` | `str` | Start time (ISO 8601) |
| `end_time` | `str` | End time (ISO 8601) |
| `description` | `str` *(optional)* | Event description |

**Response:**
```json
{
  "status": "success",
  "title": "Team Sync",
  "google_event_id": "abc123",
  "calendar_link": "https://calendar.google.com/..."
}
```

**Possible status values:**

| Status | Meaning |
|---|---|
| `success` | Event created and saved to DB |
| `failed` | Time slot was not available |
| `error` | Exception during availability check or calendar creation |
| `partial_success` | Calendar event created, but DB save failed |

---

## Project Structure

```
calendar-mcp/
├── Services/
│   └── calendar_service.py   # Google Calendar API wrappers
├── server.py                  # FastMCP server with tool definitions
├── proxy_server.py            # Optional MCP proxy (port 9000 → 8000)
├── db.py                      # Supabase persistence layer
├── client.py                  # Test/demo client
├── requirements.txt
└── .gitignore
```

---

## Dependencies

```
google-api-python-client
google-auth
google-auth-oauthlib
google-auth-httplib2
fastmcp
supabase
python-dotenv
```

---

## Notes

- All times should be in **ISO 8601 format** (e.g. `2025-06-01T10:00:00` or `2025-06-01T10:00:00+05:30`)
- The MCP server uses **HTTP transport** — no built-in authentication is included. Use the proxy layer or a reverse proxy (e.g. nginx) to add auth in production.
- The proxy server is useful for adding middleware such as authentication, logging, or rate limiting without modifying the core server.
