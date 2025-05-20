# Glance Calendar

This project provides a Glance widget that fetches and parses calendar data (iCal/VEVENT format) from a given URL.

## Features
- Accepts a URL as a query parameter
- Fetches and parses VEVENT entries from the calendar
- Returns only events with a date greater than or equal to today
- Dates are formatted as "Month Day, Year" (e.g., May 25, 2025)
- Times are formatted as "HH:MM AM/PM" (e.g., 10:00 AM)
- Dockerfile included for easy containerization

## Usage

### Run Locally
1. Install dependencies:
   ```bash
   pip install fastapi uvicorn httpx
   ```
2. Start the server:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8009
   ```
3. Access the API:
   ```
   GET http://localhost:8009/?url=<YOUR_WEBDAV_URL>
   ```

### Run with Docker
1. Build the Docker image:
   ```bash
   docker build -t glance-calendar .
   ```
2. Run the container:
   ```bash
   docker run -p 8009:8009 glance-calendar
   ```

## API
- `GET /?url=<webdav_url>`: Returns a JSON array of upcoming events with their summary, date, and time information.

## Example Response
```json
{
  "events": [
    {"summary": "Rob Dentist", "date": "May 25, 2025", "startTime": "10:00 AM", "endTime": "11:00 AM"},
    {"summary": "Team Meeting", "date": "June 1, 2025", "startTime": "09:30 AM", "endTime": "10:30 AM"}
  ]
}
```

## Example: Using the API with a Custom Template

```
- type: custom-api
  title: "Events"
  cache: 1h
  url: "http://glance-icalendar:8009/calendar?url=YOUR-URL-HERE"
  template: |
    <ul class="list list-gap-10 collapsible-container" data-collapse-after="5">
    {{ range .JSON.Array "events" }}
      <li>
        <p class="size-h4 color-highlight block text-truncate">{{ .String "summary" }}</p>
        <ul class="list-horizontal-text">
          {{ .String "date" }}
          {{ if .Has "startTime" }}
          <li>{{ .String "startTime" }}{{ if .Has "endTime" }} - {{ .String "endTime" }}{{ end }}</li>
          {{ end }}
        </ul>
      </li>
    {{ end }}
    </ul>
```

## License
MIT
