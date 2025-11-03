"""
Comprehensive unit tests for generate_ics.py

Tests cover:
- Pure functions (fold_line, escape_text, format_datetime)
- ICS generation with various configurations
- Edge cases and error handling
- File I/O operations
- Command-line argument parsing
"""

import unittest
import sys
import tempfile
import os
from pathlib import Path
from datetime import datetime, timezone as dt_timezone
from unittest.mock import patch, MagicMock, call
import io
import pytest

# Import the module under test
import generate_ics


class TestFoldLine(unittest.TestCase):
    """Test the fold_line function for iCalendar line folding."""
    
    def test_short_line_no_folding(self):
        """Short lines should not be folded."""
        line = "SHORT LINE"
        result = generate_ics.fold_line(line)
        assert result == line
    
    def test_exact_75_chars_no_folding(self):
        """Lines exactly 75 characters should not be folded."""
        line = "A" * 75
        result = generate_ics.fold_line(line)
        assert result == line
    
    def test_76_chars_folded(self):
        """Lines over 75 characters should be folded."""
        line = "A" * 76
        result = generate_ics.fold_line(line)
        expected = "A" * 75 + "\r\n " + "A"
        assert result == expected
    
    def test_very_long_line_multiple_folds(self):
        """Very long lines should be folded multiple times."""
        line = "B" * 200
        result = generate_ics.fold_line(line)
        # Should have multiple CRLF sequences
        assert "\r\n " in result
        # Each continuation line should start with space after first fold
        lines = result.split("\r\n")
        assert lines[0] == "B" * 75
        # Continuation lines start with space
        for i in range(1, len(lines)):
            assert lines[i].startswith(" ")
    
    def test_custom_max_length(self):
        """Should respect custom max_length parameter."""
        line = "C" * 50
        result = generate_ics.fold_line(line, max_length=25)
        assert "\r\n " in result
        lines = result.split("\r\n")
        assert len(lines[0]) == 25
    
    def test_empty_string(self):
        """Empty string should remain empty."""
        result = generate_ics.fold_line("")
        assert result == ""
    
    def test_unicode_characters(self):
        """Should handle unicode characters correctly."""
        line = "Event: 🎉 " * 20  # Emojis and unicode
        result = generate_ics.fold_line(line)
        # Should fold but not corrupt unicode
        assert "🎉" in result


class TestEscapeText(unittest.TestCase):
    """Test the escape_text function for iCalendar special character escaping."""
    
    def test_no_special_chars(self):
        """Text without special characters should remain unchanged."""
        text = "Normal text"
        result = generate_ics.escape_text(text)
        assert result == text
    
    def test_escape_backslash(self):
        """Backslashes should be escaped."""
        text = "path\\to\\file"
        result = generate_ics.escape_text(text)
        assert result == "path\\\\to\\\\file"
    
    def test_escape_comma(self):
        """Commas should be escaped."""
        text = "Location, City, State"
        result = generate_ics.escape_text(text)
        assert result == "Location\\, City\\, State"
    
    def test_escape_semicolon(self):
        """Semicolons should be escaped."""
        text = "Note; Important"
        result = generate_ics.escape_text(text)
        assert result == "Note\\; Important"
    
    def test_escape_newline(self):
        """Newlines should be escaped."""
        text = "Line 1\nLine 2\nLine 3"
        result = generate_ics.escape_text(text)
        assert result == "Line 1\\nLine 2\\nLine 3"
    
    def test_escape_all_special_chars(self):
        """Should escape all special characters correctly."""
        text = "Test\\with,all;special\nchars"
        result = generate_ics.escape_text(text)
        assert result == "Test\\\\with\\,all\\;special\\nchars"
    
    def test_escape_order_matters(self):
        """Backslash should be escaped first to avoid double-escaping."""
        text = "Already\\,escaped"
        result = generate_ics.escape_text(text)
        # Backslash escaped first, then comma
        assert result == "Already\\\\\\,escaped"
    
    def test_empty_string(self):
        """Empty string should return empty string."""
        result = generate_ics.escape_text("")
        assert result == ""
    
    def test_none_value(self):
        """None should return empty string."""
        result = generate_ics.escape_text(None)
        assert result == ""
    
    def test_unicode_preserved(self):
        """Unicode characters should be preserved."""
        text = "Event: 🎉, Location: Café"
        result = generate_ics.escape_text(text)
        assert result == "Event: 🎉\\, Location: Café"


class TestFormatDatetime(unittest.TestCase):
    """Test the format_datetime function for iCalendar datetime formatting."""
    
    def test_naive_datetime(self):
        """Should format naive datetime correctly."""
        dt_str = "2025-03-15T19:00:00"
        result = generate_ics.format_datetime(dt_str)
        assert result == "20250315T190000"
    
    def test_datetime_with_z_suffix(self):
        """Should handle UTC datetime with Z suffix."""
        dt_str = "2025-03-15T19:00:00Z"
        result = generate_ics.format_datetime(dt_str)
        assert result == "20250315T190000"
    
    def test_datetime_with_timezone_offset(self):
        """Should handle datetime with timezone offset."""
        dt_str = "2025-03-15T19:00:00-08:00"
        result = generate_ics.format_datetime(dt_str)
        # Should still format as local time
        assert "20250315" in result
    
    def test_datetime_with_positive_offset(self):
        """Should handle datetime with positive timezone offset."""
        dt_str = "2025-03-15T19:00:00+05:30"
        result = generate_ics.format_datetime(dt_str)
        assert "20250315" in result
    
    def test_midnight_datetime(self):
        """Should handle midnight correctly."""
        dt_str = "2025-01-01T00:00:00"
        result = generate_ics.format_datetime(dt_str)
        assert result == "20250101T000000"
    
    def test_end_of_day_datetime(self):
        """Should handle end of day correctly."""
        dt_str = "2025-12-31T23:59:59"
        result = generate_ics.format_datetime(dt_str)
        assert result == "20251231T235959"
    
    def test_invalid_datetime_exits(self):
        """Invalid datetime should exit with error."""
        with pytest.raises(SystemExit):
            generate_ics.format_datetime("invalid-date")
    
    def test_invalid_format_exits(self):
        """Incorrectly formatted datetime should exit."""
        with pytest.raises(SystemExit):
            generate_ics.format_datetime("2025/03/15 19:00")
    
    def test_timezone_parameter_unused(self):
        """Timezone parameter exists but currently unused."""
        dt_str = "2025-03-15T19:00:00"
        result = generate_ics.format_datetime(dt_str, timezone="America/Los_Angeles")
        # Should still format correctly (parameter currently not used)
        assert result == "20250315T190000"


class TestGenerateICS(unittest.TestCase):
    """Test the generate_ics function for complete .ics file generation."""
    
    def test_minimal_event(self):
        """Should generate valid ICS with only required fields."""
        result = generate_ics.generate_ics(
            title="Test Event",
            start="2025-03-15T19:00:00",
            end="2025-03-15T22:00:00",
            timezone="America/Los_Angeles"
        )
        
        # Check required components
        assert "BEGIN:VCALENDAR" in result
        assert "END:VCALENDAR" in result
        assert "BEGIN:VEVENT" in result
        assert "END:VEVENT" in result
        assert "VERSION:2.0" in result
        assert "SUMMARY:Test Event" in result
        assert "DTSTART;TZID=America/Los_Angeles:20250315T190000" in result
        assert "DTEND;TZID=America/Los_Angeles:20250315T220000" in result
        assert "STATUS:CONFIRMED" in result
        assert "UID:" in result
        assert "DTSTAMP:" in result
    
    def test_event_with_location(self):
        """Should include location when provided."""
        result = generate_ics.generate_ics(
            title="Conference",
            start="2025-06-01T09:00:00",
            end="2025-06-01T17:00:00",
            timezone="America/New_York",
            location="Convention Center, 123 Main St, New York, NY"
        )
        
        assert "LOCATION:Convention Center\\, 123 Main St\\, New York\\, NY" in result
    
    def test_event_with_description(self):
        """Should include description when provided."""
        description = "This is a test event.\nWith multiple lines.\nAnd details."
        result = generate_ics.generate_ics(
            title="Test",
            start="2025-01-01T10:00:00",
            end="2025-01-01T11:00:00",
            timezone="UTC",
            description=description
        )
        
        assert "DESCRIPTION:This is a test event.\\nWith multiple lines.\\nAnd details." in result
    
    def test_event_with_url(self):
        """Should include URL when provided."""
        result = generate_ics.generate_ics(
            title="Webinar",
            start="2025-04-10T14:00:00",
            end="2025-04-10T15:00:00",
            timezone="America/Chicago",
            url="https://example.com/event"
        )
        
        assert "URL:https://example.com/event" in result
    
    def test_event_with_organizer(self):
        """Should include organizer with email when both provided."""
        result = generate_ics.generate_ics(
            title="Meeting",
            start="2025-05-20T10:00:00",
            end="2025-05-20T11:00:00",
            timezone="Europe/London",
            organizer="John Doe",
            organizer_email="john@example.com"
        )
        
        assert "ORGANIZER;CN=John Doe:mailto:john@example.com" in result
    
    def test_event_organizer_without_email(self):
        """Should not include organizer line if email is missing."""
        result = generate_ics.generate_ics(
            title="Event",
            start="2025-07-15T16:00:00",
            end="2025-07-15T18:00:00",
            timezone="Asia/Tokyo",
            organizer="Jane Smith"
        )
        
        assert "ORGANIZER" not in result
    
    def test_event_with_categories(self):
        """Should include categories when provided."""
        result = generate_ics.generate_ics(
            title="Workshop",
            start="2025-08-01T13:00:00",
            end="2025-08-01T16:00:00",
            timezone="America/Denver",
            categories="Education,Technology,Workshop"
        )
        
        assert "CATEGORIES:Education\\,Technology\\,Workshop" in result
    
    def test_event_with_custom_status(self):
        """Should use custom status when provided."""
        result = generate_ics.generate_ics(
            title="Tentative Meeting",
            start="2025-09-05T11:00:00",
            end="2025-09-05T12:00:00",
            timezone="America/Los_Angeles",
            status="TENTATIVE"
        )
        
        assert "STATUS:TENTATIVE" in result
    
    def test_event_with_image(self):
        """Should include image URL when provided."""
        result = generate_ics.generate_ics(
            title="Conference",
            start="2025-10-10T08:00:00",
            end="2025-10-10T18:00:00",
            timezone="America/New_York",
            image="https://example.com/banner.jpg"
        )
        
        assert "IMAGE;VALUE=URI:https://example.com/banner.jpg" in result
    
    def test_event_with_single_attachment(self):
        """Should include single attachment."""
        result = generate_ics.generate_ics(
            title="Event",
            start="2025-11-15T10:00:00",
            end="2025-11-15T11:00:00",
            timezone="UTC",
            attachments=["https://example.com/agenda.pdf"]
        )
        
        assert "ATTACH;FMTTYPE=application/pdf:https://example.com/agenda.pdf" in result
    
    def test_event_with_multiple_attachments(self):
        """Should include multiple attachments with correct MIME types."""
        result = generate_ics.generate_ics(
            title="Event",
            start="2025-12-01T09:00:00",
            end="2025-12-01T10:00:00",
            timezone="America/Los_Angeles",
            attachments=[
                "https://example.com/agenda.pdf",
                "https://example.com/map.jpg",
                "https://example.com/photo.png",
                "https://example.com/document.docx",
                "https://example.com/other.txt"
            ]
        )
        
        assert "ATTACH;FMTTYPE=application/pdf:https://example.com/agenda.pdf" in result
        assert "ATTACH;FMTTYPE=image/jpeg:https://example.com/map.jpg" in result
        assert "ATTACH;FMTTYPE=image/png:https://example.com/photo.png" in result
        assert "ATTACH;FMTTYPE=application/msword:https://example.com/document.docx" in result
        assert "ATTACH:https://example.com/other.txt" in result
    
    def test_event_with_conference_url(self):
        """Should include conference URL when provided."""
        result = generate_ics.generate_ics(
            title="Virtual Meeting",
            start="2026-01-20T14:00:00",
            end="2026-01-20T15:00:00",
            timezone="America/Chicago",
            conference_url="https://zoom.us/j/123456789"
        )
        
        assert "CONFERENCE;VALUE=URI;FEATURE=VIDEO:https://zoom.us/j/123456789" in result
    
    def test_event_with_geo_coordinates(self):
        """Should include geographic coordinates when provided."""
        result = generate_ics.generate_ics(
            title="Outdoor Event",
            start="2026-02-14T12:00:00",
            end="2026-02-14T15:00:00",
            timezone="America/Los_Angeles",
            geo="37.7749,-122.4194"
        )
        
        assert "GEO:37.7749,-122.4194" in result
    
    def test_comprehensive_event(self):
        """Should handle event with all fields populated."""
        result = generate_ics.generate_ics(
            title="Complete Event",
            start="2026-03-15T09:00:00",
            end="2026-03-15T17:00:00",
            timezone="America/New_York",
            location="Grand Ballroom, 456 Park Ave, New York, NY",
            description="Full day conference with keynotes and workshops.\nRegistration required.",
            url="https://example.com/complete-event",
            organizer="Event Organizers Inc",
            organizer_email="contact@example.com",
            categories="Conference,Professional,Networking",
            status="CONFIRMED",
            image="https://example.com/event-banner.jpg",
            attachments=["https://example.com/schedule.pdf", "https://example.com/venue-map.jpg"],
            conference_url="https://zoom.us/j/987654321",
            geo="40.7589,-73.9851"
        )
        
        # Verify all fields present
        assert "SUMMARY:Complete Event" in result
        assert "LOCATION:" in result
        assert "DESCRIPTION:" in result
        assert "URL:https://example.com/complete-event" in result
        assert "ORGANIZER;CN=Event Organizers Inc:mailto:contact@example.com" in result
        assert "CATEGORIES:" in result
        assert "IMAGE;VALUE=URI:" in result
        assert "ATTACH;FMTTYPE=application/pdf:" in result
        assert "ATTACH;FMTTYPE=image/jpeg:" in result
        assert "CONFERENCE;VALUE=URI;FEATURE=VIDEO:" in result
        assert "GEO:40.7589,-73.9851" in result
    
    def test_output_to_file(self):
        """Should write ICS content to file when output_path provided."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "test_event.ics")
            
            result = generate_ics.generate_ics(
                title="File Test",
                start="2026-04-01T10:00:00",
                end="2026-04-01T11:00:00",
                timezone="UTC",
                output_path=output_path
            )
            
            # Check file was created
            assert os.path.exists(output_path)
            
            # Check file content
            with open(output_path, encoding='utf-8') as f:
                content = f.read()
            
            assert "BEGIN:VCALENDAR" in content
            assert "SUMMARY:File Test" in content
            assert content == result
    
    def test_output_ends_with_crlf(self):
        """ICS output should end with CRLF as per spec."""
        result = generate_ics.generate_ics(
            title="CRLF Test",
            start="2026-05-01T10:00:00",
            end="2026-05-01T11:00:00",
            timezone="UTC"
        )
        
        assert result.endswith('\r\n')
    
    def test_lines_use_crlf(self):
        """All line breaks should use CRLF not just LF."""
        result = generate_ics.generate_ics(
            title="Line Break Test",
            start="2026-06-01T10:00:00",
            end="2026-06-01T11:00:00",
            timezone="UTC"
        )
        
        # Should have CRLF
        assert '\r\n' in result
        # Should not have lone LF (except possibly in edge cases)
        lines = result.split('\r\n')
        for line in lines:
            assert '\n' not in line, "Found LF without CR"
    
    def test_uid_uniqueness(self):
        """Each generated event should have a unique UID."""
        result1 = generate_ics.generate_ics(
            title="Event 1",
            start="2026-07-01T10:00:00",
            end="2026-07-01T11:00:00",
            timezone="UTC"
        )
        
        result2 = generate_ics.generate_ics(
            title="Event 2",
            start="2026-07-01T12:00:00",
            end="2026-07-01T13:00:00",
            timezone="UTC"
        )
        
        # Extract UIDs
        import re
        uid1 = re.search(r'UID:([^\r\n]+)', result1).group(1)
        uid2 = re.search(r'UID:([^\r\n]+)', result2).group(1)
        
        assert uid1 != uid2
    
    def test_special_characters_in_title(self):
        """Should properly escape special characters in title."""
        result = generate_ics.generate_ics(
            title="Event: Test, Session; Part 1\nDay 2",
            start="2026-08-01T10:00:00",
            end="2026-08-01T11:00:00",
            timezone="UTC"
        )
        
        assert "SUMMARY:Event: Test\\, Session\\; Part 1\\nDay 2" in result
    
    def test_empty_attachments_list(self):
        """Should handle empty attachments list gracefully."""
        result = generate_ics.generate_ics(
            title="Event",
            start="2026-09-01T10:00:00",
            end="2026-09-01T11:00:00",
            timezone="UTC",
            attachments=[]
        )
        
        assert "ATTACH:" not in result
    
    def test_case_insensitive_attachment_extensions(self):
        """Should handle uppercase file extensions."""
        result = generate_ics.generate_ics(
            title="Event",
            start="2026-10-01T10:00:00",
            end="2026-10-01T11:00:00",
            timezone="UTC",
            attachments=["https://example.com/FILE.PDF", "https://example.com/IMAGE.JPG"]
        )
        
        assert "ATTACH;FMTTYPE=application/pdf:" in result
        assert "ATTACH;FMTTYPE=image/jpeg:" in result


class TestMain(unittest.TestCase):
    """Test the main function and CLI argument parsing."""
    
    def test_required_arguments(self):
        """Should require title, start, end, and timezone arguments."""
        test_args = ['generate_ics.py']
        with patch('sys.argv', test_args):
            with pytest.raises(SystemExit):
                generate_ics.main()
    
    def test_minimal_arguments(self):
        """Should work with just required arguments."""
        test_args = [
            'generate_ics.py',
            '--title', 'Test Event',
            '--start', '2025-03-15T19:00:00',
            '--end', '2025-03-15T22:00:00',
            '--timezone', 'America/Los_Angeles'
        ]
        
        with patch('sys.argv', test_args):
            with patch('builtins.print'):  # Suppress print output
                generate_ics.main()
    
    def test_all_arguments(self):
        """Should handle all optional arguments."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "test.ics")
            
            test_args = [
                'generate_ics.py',
                '--title', 'Complete Test',
                '--start', '2025-06-01T09:00:00',
                '--end', '2025-06-01T17:00:00',
                '--timezone', 'America/New_York',
                '--location', 'Test Venue, 123 Test St',
                '--description', 'Test description',
                '--url', 'https://example.com/event',
                '--organizer', 'Test Org',
                '--organizer-email', 'test@example.com',
                '--categories', 'Test,Event',
                '--status', 'CONFIRMED',
                '--image', 'https://example.com/image.jpg',
                '--attach', 'https://example.com/file1.pdf',
                '--attach', 'https://example.com/file2.jpg',
                '--conference', 'https://zoom.us/j/123',
                '--geo', '40.7589,-73.9851',
                '--output', output_path
            ]
            
            with patch('sys.argv', test_args):
                generate_ics.main()
            
            # Verify file was created
            assert os.path.exists(output_path)
            
            # Verify content
            with open(output_path) as f:
                content = f.read()
            
            assert 'SUMMARY:Complete Test' in content
            assert 'LOCATION:' in content
            assert 'URL:https://example.com/event' in content
    
    def test_status_choices(self):
        """Should validate status argument choices."""
        test_args = [
            'generate_ics.py',
            '--title', 'Test',
            '--start', '2025-01-01T10:00:00',
            '--end', '2025-01-01T11:00:00',
            '--timezone', 'UTC',
            '--status', 'INVALID'
        ]
        
        with patch('sys.argv', test_args):
            with pytest.raises(SystemExit):
                generate_ics.main()
    
    def test_multiple_attachments_via_cli(self):
        """Should handle multiple --attach arguments."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "test.ics")
            
            test_args = [
                'generate_ics.py',
                '--title', 'Multi Attach',
                '--start', '2025-01-01T10:00:00',
                '--end', '2025-01-01T11:00:00',
                '--timezone', 'UTC',
                '--attach', 'https://example.com/file1.pdf',
                '--attach', 'https://example.com/file2.pdf',
                '--attach', 'https://example.com/file3.pdf',
                '--output', output_path
            ]
            
            with patch('sys.argv', test_args):
                generate_ics.main()
            
            with open(output_path) as f:
                content = f.read()
            
            assert content.count('ATTACH;FMTTYPE=application/pdf:') == 3
    
    def test_output_to_stdout_when_no_file(self):
        """Should print to stdout when no output file specified."""
        test_args = [
            'generate_ics.py',
            '--title', 'Stdout Test',
            '--start', '2025-01-01T10:00:00',
            '--end', '2025-01-01T11:00:00',
            '--timezone', 'UTC'
        ]
        
        with patch('sys.argv', test_args):
            with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
                generate_ics.main()
                output = mock_stdout.getvalue()
                
                assert 'BEGIN:VCALENDAR' in output
                assert 'SUMMARY:Stdout Test' in output


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_very_long_title(self):
        """Should handle very long titles with line folding."""
        long_title = "A" * 200
        result = generate_ics.generate_ics(
            title=long_title,
            start="2025-01-01T10:00:00",
            end="2025-01-01T11:00:00",
            timezone="UTC"
        )
        
        assert long_title in result.replace('\r\n ', '')
    
    def test_very_long_description(self):
        """Should handle very long descriptions."""
        long_desc = "Description line. " * 100
        result = generate_ics.generate_ics(
            title="Test",
            start="2025-01-01T10:00:00",
            end="2025-01-01T11:00:00",
            timezone="UTC",
            description=long_desc
        )
        
        # Should contain the description (with line folding)
        assert "DESCRIPTION:" in result
    
    def test_unicode_in_all_text_fields(self):
        """Should handle unicode characters in all text fields."""
        result = generate_ics.generate_ics(
            title="Événement spécial 🎉",
            start="2025-01-01T10:00:00",
            end="2025-01-01T11:00:00",
            timezone="UTC",
            location="Café François, 日本",
            description="Descripción with émojis 🎊",
            organizer="Müller & Søren",
            categories="Célébration,文化"
        )
        
        assert "🎉" in result
        assert "François" in result
        assert "日本" in result
        assert "Descripción" in result
    
    def test_midnight_to_midnight_event(self):
        """Should handle all-day style events (midnight to midnight)."""
        result = generate_ics.generate_ics(
            title="All Day Event",
            start="2025-06-15T00:00:00",
            end="2025-06-16T00:00:00",
            timezone="UTC"
        )
        
        assert "DTSTART;TZID=UTC:20250615T000000" in result
        assert "DTEND;TZID=UTC:20250616T000000" in result
    
    def test_year_boundary(self):
        """Should handle events crossing year boundary."""
        result = generate_ics.generate_ics(
            title="New Year Event",
            start="2025-12-31T23:00:00",
            end="2026-01-01T01:00:00",
            timezone="America/New_York"
        )
        
        assert "20251231T230000" in result
        assert "20260101T010000" in result
    
    def test_leap_year_date(self):
        """Should handle leap year dates correctly."""
        result = generate_ics.generate_ics(
            title="Leap Day Event",
            start="2024-02-29T10:00:00",
            end="2024-02-29T11:00:00",
            timezone="UTC"
        )
        
        assert "20240229T100000" in result
    
    def test_whitespace_in_fields(self):
        """Should handle leading/trailing whitespace appropriately."""
        result = generate_ics.generate_ics(
            title="  Event with spaces  ",
            start="2025-01-01T10:00:00",
            end="2025-01-01T11:00:00",
            timezone="UTC",
            location="  Venue  ",
            description="  Description  "
        )
        
        # Spaces should be preserved (not our job to trim)
        assert "SUMMARY:  Event with spaces  " in result
    
    def test_empty_optional_strings(self):
        """Should handle empty strings for optional parameters."""
        result = generate_ics.generate_ics(
            title="Test",
            start="2025-01-01T10:00:00",
            end="2025-01-01T11:00:00",
            timezone="UTC",
            location="",
            description="",
            url="",
            categories=""
        )
        
        # Empty fields should result in escaped empty strings
        # Actually, empty strings should be included as empty values
        assert "LOCATION:" in result
        assert "DESCRIPTION:" in result


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflows."""
    
    def test_create_conference_event(self):
        """Integration test: Create a complete conference event."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "conference.ics")
            
            result = generate_ics.generate_ics(
                title="Python Conference 2025",
                start="2025-09-15T09:00:00",
                end="2025-09-15T17:00:00",
                timezone="America/Los_Angeles",
                location="San Francisco Convention Center, 747 Howard St, San Francisco, CA 94103",
                description="Annual Python conference featuring talks on Django, FastAPI, and more.\n\nSchedule:\n9:00 AM - Registration\n10:00 AM - Keynote\n12:00 PM - Lunch\n1:00 PM - Workshops\n5:00 PM - Closing",
                url="https://pythonconf.example.com/2025",
                organizer="Python Conference Organizers",
                organizer_email="info@pythonconf.example.com",
                categories="Conference,Programming,Python",
                status="CONFIRMED",
                image="https://pythonconf.example.com/banner.jpg",
                attachments=[
                    "https://pythonconf.example.com/schedule.pdf",
                    "https://pythonconf.example.com/venue-map.jpg"
                ],
                geo="37.7843,-122.4015",
                output_path=output_path
            )
            
            # Verify file exists and is valid
            assert os.path.exists(output_path)
            
            # Verify structure
            assert "BEGIN:VCALENDAR" in result
            assert "END:VCALENDAR" in result
            assert "BEGIN:VEVENT" in result
            assert "END:VEVENT" in result
            
            # Verify key content
            assert "Python Conference 2025" in result
            assert "San Francisco Convention Center" in result
            assert "CATEGORIES:Conference\\,Programming\\,Python" in result
    
    def test_create_virtual_meeting(self):
        """Integration test: Create a virtual meeting event."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "meeting.ics")
            
            result = generate_ics.generate_ics(
                title="Team Standup - Q1 Planning",
                start="2025-01-15T10:00:00",
                end="2025-01-15T10:30:00",
                timezone="America/New_York",
                location="Virtual - Zoom",
                description="Q1 planning discussion.\n\nJoin via Zoom:\nhttps://zoom.us/j/123456789\nMeeting ID: 123 456 789\nPasscode: standup2025",
                organizer="Team Lead",
                organizer_email="lead@company.com",
                conference_url="https://zoom.us/j/123456789",
                status="CONFIRMED",
                output_path=output_path
            )
            
            # Verify structure
            assert os.path.exists(output_path)
            assert "Virtual - Zoom" in result
            assert "CONFERENCE;VALUE=URI;FEATURE=VIDEO:https://zoom.us/j/123456789" in result
            assert "Q1 planning discussion" in result
    
    def test_create_concert_event(self):
        """Integration test: Create a concert/entertainment event."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "concert.ics")
            
            result = generate_ics.generate_ics(
                title="The Beatles Tribute Night",
                start="2025-07-20T20:00:00",
                end="2025-07-20T23:00:00",
                timezone="Europe/London",
                location="Royal Albert Hall, Kensington Gore, London SW7 2AP",
                description="Experience the magic of The Beatles with a full tribute performance.\n\nPerforming:\n- All the hits from the 60s\n- Full costume and stage production\n- Special acoustic set\n\nDoors open at 7:00 PM.",
                url="https://tickets.example.com/beatles-tribute",
                organizer="Royal Albert Hall Events",
                categories="Concert,Music,Entertainment",
                image="https://tickets.example.com/beatles-poster.jpg",
                geo="51.5009,-0.1773",
                output_path=output_path
            )
            
            assert os.path.exists(output_path)
            assert "The Beatles Tribute Night" in result
            assert "Royal Albert Hall" in result
            assert "Concert\\,Music\\,Entertainment" in result


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)