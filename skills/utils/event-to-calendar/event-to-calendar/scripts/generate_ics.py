#!/usr/bin/env python3
"""
Generate .ics calendar files with comprehensive event information.

Usage:
    python generate_ics.py \
        --title "Event Name" \
        --start "2025-03-15T19:00:00" \
        --end "2025-03-15T22:00:00" \
        --timezone "America/Los_Angeles" \
        --location "The Fillmore, 1805 Geary Blvd, San Francisco, CA 94115" \
        --description "Event description with full details" \
        --url "https://example.com/event" \
        --organizer "Organizer Name" \
        --organizer-email "organizer@example.com" \
        --image "https://example.com/event-banner.jpg" \
        --attach "https://example.com/agenda.pdf" \
        --attach "https://example.com/parking.pdf" \
        --conference "https://zoom.us/j/123456789" \
        --geo "37.7749,-122.4194" \
        --output "event.ics"
"""

import argparse
import sys
from datetime import datetime, timezone as dt_timezone
from pathlib import Path
import uuid
import re


def fold_line(line, max_length=75):
    """
    Fold lines to meet iCalendar 75-character limit per line.
    Continuation lines start with a space.
    """
    if len(line) <= max_length:
        return line
    
    result = []
    current = line
    
    while len(current) > max_length:
        # Find a safe break point (not in the middle of a multi-byte character)
        break_point = max_length
        result.append(current[:break_point])
        current = ' ' + current[break_point:]  # Continuation lines start with space
    
    result.append(current)
    return '\r\n'.join(result)


def escape_text(text):
    """Escape special characters for iCalendar format."""
    if not text:
        return ""
    # Escape backslashes first, then commas, semicolons, and newlines
    text = text.replace('\\', '\\\\')
    text = text.replace(',', '\\,')
    text = text.replace(';', '\\;')
    text = text.replace('\n', '\\n')
    return text


def format_datetime(dt_str, timezone=None):
    """
    Convert an ISO-like datetime string to iCalendar DATETIME format (YYYYMMDDTHHMMSS).
    
    Accepts ISO 8601 datetime strings that may be naive or include timezone information (for example "2025-03-15T19:00:00" or "2025-03-15T19:00:00Z"). The optional `timezone` parameter is accepted for API compatibility but is not used by this function.
    
    Parameters:
        dt_str (str): ISO-like datetime string to convert.
        timezone (str | None): Ignored; retained for compatibility.
    
    Returns:
        str: Datetime formatted as `YYYYMMDDTHHMMSS`.
    
    Raises:
        SystemExit: Exits with code 1 after printing a parse error to stderr if `dt_str` cannot be parsed.
    """
    try:
        # Parse the datetime, handling both naive and timezone-aware strings
        if 'Z' in dt_str or '+' in dt_str or dt_str.count('-') > 2:
            # Already has timezone info
            dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        else:
            # Naive datetime
            dt = datetime.fromisoformat(dt_str)
        return dt.strftime('%Y%m%dT%H%M%S')
    except ValueError as e:
        print(f"Error parsing datetime '{dt_str}': {e}", file=sys.stderr)
        sys.exit(1)

def generate_ics(
    title,
    start,
    end,
    timezone,
    location=None,
    description=None,
    url=None,
    organizer=None,
    organizer_email=None,
    categories=None,
    status="CONFIRMED",
    image=None,
    attachments=None,
    conference_url=None,
    geo=None,
    output_path=None
):
    """
    Generate a complete iCalendar (ICS) event and return its contents as a string.
    
    Parameters:
        title (str): Event summary/title.
        start (str): Start datetime in an ISO-like format parseable by format_datetime.
        end (str): End datetime in an ISO-like format parseable by format_datetime.
        timezone (str): Time zone identifier used for DTSTART/DTEND (added as TZID).
        location (str, optional): Event location.
        description (str, optional): Event description; special characters will be escaped for ICS.
        url (str, optional): URL associated with the event.
        organizer (str, optional): Organizer common name.
        organizer_email (str, optional): Organizer email address (used if provided).
        categories (str, optional): Comma-separated categories for the event.
        status (str, optional): Event status (defaults to "CONFIRMED").
        image (str, optional): URI to an image to include via IMAGE property.
        attachments (list[str], optional): List of attachment URIs; MIME type may be inferred from file extensions.
        conference_url (str, optional): URI for a conference/meeting link (added as CONFERENCE).
        geo (str, optional): Geographic coordinates for the event (included verbatim in the GEO property).
        output_path (str, optional): If provided, write the ICS content to this file path.
    
    Returns:
        ics_content (str): The serialized ICS content (CRLF line endings, folded to 75 characters).
    """
    
    # Generate unique identifier
    uid = f"{uuid.uuid4()}@claude.ai"
    
    # Current timestamp
    dtstamp = datetime.now(dt_timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    
    # Format datetimes
    dtstart_formatted = format_datetime(start, timezone)
    dtend_formatted = format_datetime(end, timezone)
    
    # Build the VEVENT
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Claude//Event to Calendar Skill//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "BEGIN:VEVENT",
        f"UID:{uid}",
        f"DTSTAMP:{dtstamp}",
        f"DTSTART;TZID={timezone}:{dtstart_formatted}",
        f"DTEND;TZID={timezone}:{dtend_formatted}",
        f"SUMMARY:{escape_text(title)}",
        f"STATUS:{status}",
    ]
    
    # Add optional fields
    if location:
        lines.append(f"LOCATION:{escape_text(location)}")
    
    if description:
        lines.append(f"DESCRIPTION:{escape_text(description)}")
    
    if url:
        lines.append(f"URL:{url}")
    
    if organizer:
        if organizer_email:
            lines.append(f"ORGANIZER;CN={escape_text(organizer)}:mailto:{organizer_email}")
        else:
            lines.append(f"ORGANIZER;CN={escape_text(organizer)}:invalid:nomail")
    
    if categories:
        lines.append(f"CATEGORIES:{escape_text(categories)}")
    
    if image:
        lines.append(f"IMAGE;VALUE=URI:{image}")
    
    if attachments:
        for attachment in attachments:
            # Try to determine MIME type from URL extension
            if attachment.lower().endswith('.pdf'):
                lines.append(f"ATTACH;FMTTYPE=application/pdf:{attachment}")
            elif attachment.lower().endswith(('.jpg', '.jpeg')):
                lines.append(f"ATTACH;FMTTYPE=image/jpeg:{attachment}")
            elif attachment.lower().endswith('.png'):
                lines.append(f"ATTACH;FMTTYPE=image/png:{attachment}")
            elif attachment.lower().endswith(('.doc', '.docx')):
                lines.append(f"ATTACH;FMTTYPE=application/msword:{attachment}")
            else:
                lines.append(f"ATTACH:{attachment}")
    
    if conference_url:
        lines.append(f"CONFERENCE;VALUE=URI;FEATURE=VIDEO:{conference_url}")
    
    if geo:
        lines.append(f"GEO:{geo}")
    
    lines.extend([
        "END:VEVENT",
        "END:VCALENDAR"
    ])
    
    # Fold long lines
    folded_lines = []
    for line in lines:
        folded_lines.append(fold_line(line))
    
    # Join with CRLF as per iCalendar spec
    ics_content = '\r\n'.join(folded_lines) + '\r\n'
    
    # Write to file
    if output_path:
        output_file = Path(output_path)
        output_file.write_text(ics_content, encoding='utf-8')
        print(f"✅ Calendar file created: {output_file.absolute()}")
    else:
        print(ics_content)
    
    return ics_content


def main():
    """
    Parse command-line arguments for event properties and create an iCalendar (.ics) file or print it to stdout.
    
    The function defines and parses required arguments (--title, --start, --end, --timezone) and several optional arguments (location, description, url, organizer and organizer email, categories, status, image, attachments, conference URL, geo coordinates, and output path) and then generates the corresponding .ics content which is written to the given output file when --output is provided or emitted to standard output otherwise.
    """
    parser = argparse.ArgumentParser(
        description='Generate .ics calendar files with comprehensive event information.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Required arguments
    parser.add_argument('--title', required=True, help='Event title/name')
    parser.add_argument('--start', required=True, help='Start datetime (ISO format: 2025-03-15T19:00:00)')
    parser.add_argument('--end', required=True, help='End datetime (ISO format: 2025-03-15T22:00:00)')
    parser.add_argument('--timezone', required=True, help='Timezone (e.g., America/Los_Angeles)')
    
    # Optional arguments
    parser.add_argument('--location', help='Event location (venue name and/or address)')
    parser.add_argument('--description', help='Detailed event description')
    parser.add_argument('--url', help='Event URL')
    parser.add_argument('--organizer', help='Organizer name')
    parser.add_argument('--organizer-email', help='Organizer email address')
    parser.add_argument('--categories', help='Event categories/tags (comma-separated)')
    parser.add_argument('--status', default='CONFIRMED', choices=['CONFIRMED', 'TENTATIVE', 'CANCELLED'],
                       help='Event status')
    parser.add_argument('--image', help='Event image URL (banner, logo, poster)')
    parser.add_argument('--attach', action='append', dest='attachments',
                       help='Attachment URLs (can be used multiple times for multiple attachments)')
    parser.add_argument('--conference', dest='conference_url',
                       help='Video conference URL (Zoom, Teams, etc.)')
    parser.add_argument('--geo', help='Geographic coordinates as "latitude,longitude" (e.g., "37.7749,-122.4194")')
    parser.add_argument('--output', '-o', help='Output file path (default: stdout)')
    
    args = parser.parse_args()
    
    generate_ics(
        title=args.title,
        start=args.start,
        end=args.end,
        timezone=args.timezone,
        location=args.location,
        description=args.description,
        url=args.url,
        organizer=args.organizer,
        organizer_email=args.organizer_email,
        categories=args.categories,
        status=args.status,
        image=args.image,
        attachments=args.attachments,
        conference_url=args.conference_url,
        geo=args.geo,
        output_path=args.output
    )


if __name__ == '__main__':
    main()