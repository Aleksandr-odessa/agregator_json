from logsjs.models import LogEntry
from io import StringIO
import json
from unittest import mock
from django.core.management import call_command
from django.test import TestCase


class LogEntryCommandTests(TestCase):

    @mock.patch('aiohttp.ClientSession.get')
    async def async_test_fetch_log(self, mock_get):
            """Test to ensure fetch_log yields correct lines."""
            # Mocking the log file response
            async def mock_async_generator():
                for line in [
                    json.dumps({
                        "remote_ip": "192.168.0.1",
                        "time": "03/Dec/2023:19:01:01",
                        "request": "GET /index.html HTTP/1.1",
                        "response": "200",
                        "bytes": "1024"
                    }).encode('utf-8'),
                    b'',
                    json.dumps({
                        "remote_ip": "192.168.0.2",
                        "time": "03/Dec/2023:19:02:02",
                        "request": "POST /submit HTTP/1.1",
                        "response": "404",
                        "bytes": "512"
                    }).encode('utf-8'),
                ]:
                    yield line

            # Call the handle command with the mocked URL
            with mock.patch('sys.stdout'):
                # call_command('your_command_name', 'http://mocked-log-url.com')
                call_command('parse_log', 'http://127.0.0.1:8000/download/')


            # Assert data in the database
            self.assertEqual(LogEntry.objects.count(), 2)

            # Assert that the first entry is correct
            entry = LogEntry.objects.first()
            self.assertEqual(entry.ip_address, "192.168.0.1")
            self.assertEqual(entry.http_method, "GET")
            self.assertEqual(entry.uri, "/index.html")
            self.assertEqual(entry.response_code, 200)
            self.assertEqual(entry.response_size, 1024)

    def test_my_command_output(self):
        out = StringIO()
        call_command('parse_log', 'http://127.0.0.1:8000/download/', stdout=out)
        self.assertIn("Successfully parsed and saved log entries", out.getvalue())
