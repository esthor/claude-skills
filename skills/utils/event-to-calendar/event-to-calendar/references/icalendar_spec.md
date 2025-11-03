# iCalendar (.ics) Format Reference

Quick reference for the iCalendar format used in .ics files.

## Basic Structure

```
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Your Organization//Product//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
BEGIN:VEVENT
[event properties]
END:VEVENT
END:VCALENDAR
```

## Essential VEVENT Properties

### Required Properties

- **UID** - Unique identifier for the event
  - Format: `UID:unique-id@domain.com`
  - Example: `UID:20250315T190000-001@example.com`

- **DTSTAMP** - Timestamp when the event was created
  - Format: UTC datetime with 'Z' suffix
  - Example: `DTSTAMP:20251102T120000Z`

- **DTSTART** - Event start date/time
  - With timezone: `DTSTART;TZID=America/Los_Angeles:20250315T190000`
  - UTC: `DTSTART:20250315T190000Z`
  - All-day event: `DTSTART;VALUE=DATE:20250315`

- **DTEND** or **DURATION** - Event end (use one, not both)
  - DTEND with timezone: `DTEND;TZID=America/Los_Angeles:20250315T220000`
  - DURATION: `DURATION:PT3H` (3 hours)

- **SUMMARY** - Event title/name
  - Example: `SUMMARY:Annual Tech Conference 2025`

### Important Optional Properties

- **LOCATION** - Physical or virtual location
  - Example: `LOCATION:Moscone Center\, 747 Howard St\, San Francisco\, CA`

- **DESCRIPTION** - Detailed event description
  - Example: `DESCRIPTION:Join us for keynote speakers\, workshops\, and networking.`

- **URL** - Link to event website
  - Example: `URL:https://example.com/event`

- **ORGANIZER** - Event organizer with contact info
  - With name: `ORGANIZER;CN=John Doe:mailto:john@example.com`
  - Without email: `ORGANIZER;CN=John Doe:invalid:nomail`

- **CATEGORIES** - Event classification tags
  - Example: `CATEGORIES:Conference\,Technology\,Networking`

- **STATUS** - Event status
  - Values: `CONFIRMED`, `TENTATIVE`, `CANCELLED`
  - Example: `STATUS:CONFIRMED`

- **CLASS** - Access classification
  - Values: `PUBLIC`, `PRIVATE`, `CONFIDENTIAL`
  - Example: `CLASS:PUBLIC`

- **PRIORITY** - Event priority (0-9, where 0 is undefined)
  - Example: `PRIORITY:5`

### Multimedia and Rich Content Properties

- **IMAGE** - Event image/banner (RFC 7986)
  - Example: `IMAGE;VALUE=URI:https://example.com/event-banner.jpg`

- **ATTACH** - Attached documents, files, or links
  - With MIME type: `ATTACH;FMTTYPE=application/pdf:https://example.com/agenda.pdf`
  - Multiple attachments: Add multiple ATTACH properties
  - Example: 
    ```
    ATTACH;FMTTYPE=application/pdf:https://example.com/agenda.pdf
    ATTACH;FMTTYPE=image/jpeg:https://example.com/venue-map.jpg
    ATTACH;FMTTYPE=application/msword:https://example.com/handout.docx
    ```

- **CONFERENCE** - Video conference/meeting URL (RFC 7986)
  - Example: `CONFERENCE;VALUE=URI;FEATURE=VIDEO:https://zoom.us/j/123456789`
  - For audio: `CONFERENCE;VALUE=URI;FEATURE=AUDIO:tel:+1-234-567-8900`

- **GEO** - Geographic coordinates (latitude;longitude)
  - Example: `GEO:37.7749;-122.4194`
  - Enables "Get Directions" in calendar apps

## Datetime Formats

### Basic Formats

- **Local time**: `20250315T190000`
- **UTC time**: `20250315T190000Z` (note the Z suffix)
- **With timezone**: `DTSTART;TZID=America/Los_Angeles:20250315T190000`
- **Date only** (all-day): `20250315`

### Common Timezones

Use IANA timezone identifiers:
- `America/Los_Angeles` (Pacific)
- `America/New_York` (Eastern)
- `America/Chicago` (Central)
- `Europe/London` (GMT/BST)
- `Asia/Tokyo` (JST)
- `UTC` (Coordinated Universal Time)

## Text Escaping

Special characters must be escaped:

- Backslash: `\\` → `\\\\`
- Comma: `,` → `\\,`
- Semicolon: `;` → `\\;`
- Newline: `\n` → `\\n`

Example:
```
LOCATION:Venue Name\, 123 Main St\, City\, State
DESCRIPTION:First line\\nSecond line\\nThird line
```

## Line Folding

Lines must not exceed 75 octets (characters). Long lines are folded:

```
DESCRIPTION:This is a very long description that needs to be folded because
  it exceeds the 75 character limit per line in the iCalendar format specif
 ication.
```

Continuation lines start with a space or tab.

## Recurring Events

Use RRULE for recurring events:

### Daily
```
RRULE:FREQ=DAILY;COUNT=10
```

### Weekly (every Monday and Wednesday)
```
RRULE:FREQ=WEEKLY;BYDAY=MO,WE;COUNT=10
```

### Monthly (on the 15th)
```
RRULE:FREQ=MONTHLY;BYMONTHDAY=15;COUNT=6
```

### Yearly
```
RRULE:FREQ=YEARLY;BYMONTH=12;BYMONTHDAY=25;COUNT=5
```

### Until a date
```
RRULE:FREQ=DAILY;UNTIL=20251231T235959Z
```

## Multi-day Events

For events spanning multiple days:

```
DTSTART;TZID=America/Los_Angeles:20250315T090000
DTEND;TZID=America/Los_Angeles:20250317T170000
```

Or for all-day multi-day events:
```
DTSTART;VALUE=DATE:20250315
DTEND;VALUE=DATE:20250318
```
Note: DTEND is exclusive (event ends before this date)

## Alarms/Reminders

Add VALARM components inside VEVENT:

```
BEGIN:VALARM
TRIGGER:-PT15M
ACTION:DISPLAY
DESCRIPTION:Event reminder
END:VALARM
```

Common trigger values:
- `-PT15M` - 15 minutes before
- `-PT1H` - 1 hour before
- `-P1D` - 1 day before

## Virtual Events

For online events, include connection details:

```
LOCATION:Virtual Event
DESCRIPTION:Join via Zoom: https://zoom.us/j/123456789\\nMeeting ID: 123 4
 56 789\\nPasscode: abc123
URL:https://zoom.us/j/123456789
```

## Complete Example

### Basic Event

```
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Claude//Event to Calendar Skill//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
BEGIN:VEVENT
UID:20250315T190000-tech-conf@example.com
DTSTAMP:20251102T120000Z
DTSTART;TZID=America/Los_Angeles:20250315T190000
DTEND;TZID=America/Los_Angeles:20250315T220000
SUMMARY:Annual Tech Conference 2025
LOCATION:Moscone Center\, 747 Howard St\, San Francisco\, CA 94103
DESCRIPTION:Join us for keynote presentations on AI\, cloud computing\, an
 d the future of software development. Registration includes access to all 
 workshops and networking sessions.\\n\\nSchedule:\\n9:00 AM - Registration
 \\n10:00 AM - Keynote\\n12:00 PM - Lunch\\n1:00 PM - Workshops\\n5:00 PM 
 - Networking
URL:https://example.com/techconf2025
ORGANIZER;CN=Tech Events Inc:mailto:events@techevents.com
STATUS:CONFIRMED
CATEGORIES:Conference\,Technology\,Networking
CLASS:PUBLIC
BEGIN:VALARM
TRIGGER:-PT1H
ACTION:DISPLAY
DESCRIPTION:Conference starts in 1 hour
END:VALARM
END:VEVENT
END:VCALENDAR
```

### Rich Event with Multimedia

```
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Claude//Event to Calendar Skill//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
BEGIN:VEVENT
UID:20250620T090000-ai-workshop@example.com
DTSTAMP:20251102T120000Z
DTSTART;TZID=America/New_York:20250620T090000
DTEND;TZID=America/New_York:20250620T170000
SUMMARY:AI Summit 2025 - Advanced Workshop
LOCATION:Jacob Javits Center\, Room 3B\, 429 11th Ave\, New York\, NY 1000
 1
DESCRIPTION:Full-day intensive workshop on transformer architectures and la
 rge language models. Includes hands-on coding sessions\, guest speakers\, 
 and networking lunch.\\n\\nPrerequisites: Python programming experience an
 d basic ML knowledge.
URL:https://example.com/ai-summit/workshop
ORGANIZER;CN=AI Summit Organizers:mailto:workshops@aisummit.org
STATUS:CONFIRMED
CATEGORIES:Workshop\,AI\,Machine Learning
IMAGE;VALUE=URI:https://example.com/images/ai-summit-banner.jpg
ATTACH;FMTTYPE=application/pdf:https://example.com/materials/agenda.pdf
ATTACH;FMTTYPE=application/pdf:https://example.com/materials/prerequisites
 .pdf
ATTACH;FMTTYPE=image/jpeg:https://example.com/materials/venue-map.jpg
CONFERENCE;VALUE=URI;FEATURE=VIDEO:https://zoom.us/j/987654321
GEO:40.7560;-73.9965
CLASS:PUBLIC
END:VEVENT
END:VCALENDAR
```

## Best Practices

1. **Always use TZID** for local times rather than UTC conversion when timezone is known
2. **Include rich descriptions** with all relevant details (schedule, speakers, requirements)
3. **Add the event URL** for reference
4. **Use proper escaping** for special characters
5. **Fold long lines** to stay within 75 character limit
6. **Include organizer contact** information when available
7. **Add categories** to help with event organization
8. **Set appropriate alarms** for important events
9. **Add multimedia content** when available:
   - Event images/banners for visual appeal
   - Attachments for agendas, maps, materials
   - Conference URLs for virtual/hybrid events
   - Geo coordinates for precise mapping
10. **Link to relevant resources** (venue website, parking info, registration)
11. **Keep attachments reasonable** - link to large files rather than embedding

## Common Mistakes to Avoid

- ❌ Missing required fields (UID, DTSTAMP, DTSTART)
- ❌ Incorrect timezone format
- ❌ Forgetting to escape special characters
- ❌ Lines exceeding 75 characters without folding
- ❌ Using both DTEND and DURATION (use only one)
- ❌ Incomplete location information
- ❌ Sparse descriptions that don't provide context
- ❌ Missing CRLF line endings (must be `\r\n`)

## Resources

- RFC 5545: Internet Calendaring and Scheduling Core Object Specification
- IANA Timezone Database: https://www.iana.org/time-zones
