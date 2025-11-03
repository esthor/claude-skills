---
name: event-to-calendar
description: Extract comprehensive event information from website URLs and generate rich .ics calendar files. Use when users provide an event URL (conference, concert, meetup, webinar, sports event, etc.) and want to add it to their calendar. Creates detailed calendar events with all relevant information (title, date/time, location, description, organizer, URL) so users don't need to visit the website.
---

# Event to Calendar

Extract event information from websites and generate rich, complete .ics calendar files that users can import directly into their calendar applications.

## Core Workflow

### 1. Fetch Event Information

When given an event URL, use `web_fetch` to retrieve the complete webpage content:

```python
# Always fetch the full page content
web_fetch(url=event_url)
```

### 2. Extract All Relevant Information

Parse the fetched content to extract ALL of the following fields. Leave no field unextracted if it's available on the page:

**Required fields:**
- **Event title/name** - The official event name
- **Start date and time** - Full datetime with timezone
- **End date and time** - Full datetime with timezone (estimate if not provided)

**Critical optional fields (extract whenever available):**
- **Location** - Full address or venue name with details (room number, floor, building)
- **Description** - Rich description including:
  - Event overview/summary
  - Speaker/performer information
  - Schedule/agenda highlights
  - What to expect
  - Registration details or requirements
  - Any important notes or instructions
- **Organizer** - Person, company, or organization hosting the event
- **Event URL** - Original event page for reference
- **Event type** - Conference, concert, meetup, webinar, sports, etc.
- **Timezone** - Explicit timezone (critical for accuracy)

**Additional enrichment fields:**
- **Categories/tags** - Event type classifications
- **Status** - CONFIRMED, TENTATIVE, CANCELLED
- **Contact information** - Email or phone for the organizer
- **Cost/ticket information** - Free, paid, registration required, etc.
- **Capacity/attendance limits**
- **Special instructions** - Parking info, what to bring, dress code, etc.

**Multimedia and attachments:**
- **Event image/logo** - Visual identifier for the event
- **Attachments** - Documents, agendas, slides, maps, tickets
- **Additional URLs** - Registration, livestream, materials, venue website
- **Video conference details** - Zoom/Teams/Meet links with meeting IDs
- **Geographic coordinates** - Latitude/longitude for precise location
- **Attendee information** - Speaker/organizer profiles if available

### 3. Double-Check Extracted Information

CRITICAL: Before generating the .ics file, systematically verify each extracted field:

1. **Date/time verification**:
   - Confirm dates are in the future (unless it's a past event)
   - Verify start time comes before end time
   - Check timezone is correct and explicitly stated
   - Ensure AM/PM is correct
   - Validate day of week matches the date

2. **Location verification**:
   - Ensure address is complete and properly formatted
   - Include venue name AND address if both available
   - Add room/floor details if specified

3. **Description completeness**:
   - Include enough context that the user doesn't need to visit the website
   - Add speaker names, session titles, or key highlights
   - Include any registration or attendance requirements

4. **URL verification**:
   - Ensure the event URL is included for reference
   - Add registration URL if different from main event page

### 4. Generate the .ics File

Use the provided script to generate a properly formatted .ics file:

```python
# Call the calendar generation script with all extracted data
bash_tool(
    command=f"python3 /home/claude/event-to-calendar/scripts/generate_ics.py ...",
    description="Generating .ics calendar file with all event details"
)
```

See `scripts/generate_ics.py` for the complete implementation.

### 5. Present to User

Save the generated .ics file to `/mnt/user-data/outputs/` and provide:

1. A confirmation of the event details extracted
2. A direct download link to the .ics file
3. A summary of key information (date, time, location)

Example response:
```
I've created a calendar event for [Event Name].

**Event Details:**
- Date: Friday, March 15, 2025
- Time: 7:00 PM - 10:00 PM PST
- Location: The Fillmore, 1805 Geary Blvd, San Francisco, CA 94115

[Download calendar file](computer:///mnt/user-data/outputs/event-name.ics)

The calendar event includes the full description, speaker information, and event URL so you have everything you need.
```

## Quality Standards

### Completeness Checklist

Before finalizing, verify the .ics file includes:

- ✅ Event title (SUMMARY)
- ✅ Start datetime with timezone (DTSTART)
- ✅ End datetime with timezone (DTEND)
- ✅ Location with full details (LOCATION)
- ✅ Rich description with context (DESCRIPTION)
- ✅ Event URL (URL)
- ✅ Organizer information (ORGANIZER)
- ✅ Unique identifier (UID)
- ✅ Timestamp (DTSTAMP)
- ✅ Categories/tags if applicable (CATEGORIES)

### Common Pitfalls to Avoid

1. **Timezone confusion**: Always include explicit timezone in DTSTART/DTEND
2. **Incomplete descriptions**: Don't just copy the title - include full context
3. **Missing location details**: Include venue name AND address, plus room/floor
4. **Duration estimates**: If end time not specified, estimate reasonable duration (e.g., 1-2 hours for talks, 3-4 hours for conferences)
5. **URL omission**: Always include the original event URL for reference
6. **Date format errors**: Use proper iCalendar datetime format (YYYYMMDDTHHMMSS)

## Advanced Features

### Multi-day Events

For conferences or festivals spanning multiple days:
- Set DTSTART to first day start time
- Set DTEND to last day end time
- Include daily schedule in description
- Consider noting "Multi-day event" in description

### Recurring Events

For recurring meetups or classes:
- Include RRULE for recurrence pattern if clear from website
- Document the recurrence schedule in description
- Note any exceptions or holidays

### Virtual Events

For online events (webinars, virtual conferences):
- Use "VIRTUAL" or "Online Event" in location field
- Include video conference link in description
- Add platform information (Zoom, Teams, etc.)
- Include dial-in numbers or meeting IDs if provided

### Multimedia Enrichment

Modern calendar applications support rich content that makes events more useful:

**Images:**
- Event logos or banners
- Venue photos
- Speaker headshots
- Event posters

Add via ATTACH property with image URLs or IMAGE property:
```
ATTACH:https://example.com/event-logo.png
IMAGE;VALUE=URI:https://example.com/banner.jpg
```

**Documents and Materials:**
- PDF agendas or schedules
- Presentation slides
- Registration confirmations
- Venue maps or parking passes
- Background reading materials

Add multiple attachments:
```
ATTACH;FMTTYPE=application/pdf:https://example.com/agenda.pdf
ATTACH;FMTTYPE=application/pdf:https://example.com/parking-pass.pdf
```

**Additional URLs:**
Beyond the main event URL, include:
- Registration/RSVP links
- Livestream URLs
- Venue website
- Hotel booking links
- Transportation/parking info

**Video Conference Details:**
For hybrid or virtual events, use CONFERENCE property:
```
CONFERENCE;VALUE=URI;FEATURE=VIDEO:https://zoom.us/j/123456789
CONFERENCE;VALUE=URI;FEATURE=AUDIO:tel:+1-234-567-8900,,123456789#
```

Or include richly formatted in description:
```
Join via Zoom: https://zoom.us/j/123456789
Meeting ID: 123 456 789
Passcode: abc123
```

**Geographic Coordinates:**
Add precise location for mapping:
```
GEO:37.7749;-122.4194
```

This enables "Get Directions" features in calendar apps.

**Best Practices for Rich Events:**
1. Extract images when prominently featured on event page
2. Look for downloadable materials (agendas, slides, maps)
3. Include multiple ways to join virtual events
4. Add geo coordinates for venues when address is available
5. Link to related resources (venue website, hotel booking)
6. Keep file sizes reasonable (link to large files, don't embed)

## Technical Notes

### iCalendar Format Basics

- Each .ics file starts with `BEGIN:VCALENDAR` and ends with `END:VCALENDAR`
- Events are wrapped in `BEGIN:VEVENT` and `END:VEVENT`
- Lines must not exceed 75 characters (fold long lines)
- Times can be in UTC (with Z suffix) or with explicit TZID
- Use `\n` for line breaks in descriptions

### Timezone Handling

Prefer explicit timezone information:
```
DTSTART;TZID=America/Los_Angeles:20250315T190000
```

Rather than UTC conversion unless timezone is unknown.

## References

For detailed .ics format specifications, see `references/icalendar_spec.md`.
