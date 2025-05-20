from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
import httpx
import uvicorn
import logging
import xml.etree.ElementTree as ET
from datetime import datetime

app = FastAPI()

@app.get("/calendar")
async def get_webdav_content(url: str = Query(..., description="WebDAV resource URL")):
    print(f"Received URL: {url}")  # Log the received URL
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(url)
            response.raise_for_status()
            content = response.text
        # Parse WebDAV VEVENT response
        events = []
        today = datetime.now().date()
        for block in content.split("BEGIN:VEVENT"):
            if "END:VEVENT" not in block:
                continue
            summary = None
            date = None
            dt_obj = None
            startTime = None
            endTime = None
            for line in block.splitlines():
                if line.startswith("SUMMARY:"):
                    summary = line[len("SUMMARY:"):].strip()
                elif line.startswith("DTSTART"):
                    dt_raw = line.split(":", 1)[-1].strip()
                    try:
                        # Check if time information is included (format: YYYYMMDDTHHMMSS)
                        if len(dt_raw) > 8 and 'T' in dt_raw:
                            # Parse date and time
                            full_dt = datetime.strptime(dt_raw[:15], "%Y%m%dT%H%M%S")
                            dt_obj = full_dt.date()
                            date = dt_obj.strftime("%B %d, %Y")
                            startTime = full_dt.strftime("%I:%M %p")  # Format: 12:00 PM
                        else:
                            # Only date, no time
                            dt_obj = datetime.strptime(dt_raw[:8], "%Y%m%d").date()
                            date = dt_obj.strftime("%B %d, %Y")
                    except Exception:
                        date = None
                elif line.startswith("DTEND"):
                    dt_raw = line.split(":", 1)[-1].strip()
                    try:
                        if len(dt_raw) > 8 and 'T' in dt_raw:
                            end_dt = datetime.strptime(dt_raw[:15], "%Y%m%dT%H%M%S")
                            endTime = end_dt.strftime("%I:%M %p")  # Format: 12:00 PM
                    except Exception:
                        endTime = None
            # Only include if date is today or in the future
            if summary and date and dt_obj:
                if dt_obj >= today:
                    event_data = {"summary": summary, "date": date, "_dt_obj": dt_obj}
                    if startTime:
                        event_data["startTime"] = startTime
                    if endTime:
                        event_data["endTime"] = endTime
                    events.append(event_data)
        # Sort events by date ascending
        events.sort(key=lambda x: x["_dt_obj"])
        # Remove the helper _dt_obj before returning
        for event in events:
            event.pop("_dt_obj", None)
        print(f"Parsed events: {events}")  # Log the parsed events
        return JSONResponse(content={"events": events})
    except httpx.HTTPError as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8009, reload=True)