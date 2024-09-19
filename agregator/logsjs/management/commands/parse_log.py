import asyncio
import json

import aiohttp
from datetime import datetime

import requests
from asgiref.sync import sync_to_async
from django.core.management.base import BaseCommand

import logging

from logsjs.models import LogEntry

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Parses an Nginx log file and stores the entries in the database."

    def add_arguments(self, parser):
        parser.add_argument('link_to_file', type=str, help='Link to the log file')

    async def fetch_log(self, session, url):
        async with session.get(url) as response:
            async for line in response.content:
                yield line.decode('utf-8')


    def handle(self, *args, **kwargs):
        link_to_logfile = kwargs['link_to_file']
        asyncio.run(self.process_log(link_to_logfile))
        self.stdout.write(self.style.SUCCESS("Successfully parsed and saved log entries"))


    async def process_log(self, url):
        log_entries = []
        batch_size = 1000
        async with aiohttp.ClientSession() as session:
            async for line in self.fetch_log(session, url):
                if line.strip():
                    try:
                        data = json.loads(line.strip())
                    except json.JSONDecodeError:
                        logger.error("Failed to decode JSON")
                    request_list = data["request"].split(" ")
                    try:
                        timestamp = datetime.strptime(data["time"].split(" ")[0], "%d/%b/%Y:%H:%M:%S")
                    except ValueError:
                        logger.error("Failed to parse timestamp")
                        log_entry = LogEntry(
                            ip_address=data['remote_ip'],
                            timestamp=timestamp,
                            http_method=request_list[0],
                            uri=request_list[1],
                            response_code=int(data['response']),
                            response_size=int(data['bytes']),
                        )
                        log_entries.append(log_entry)
                        if len(log_entries) >= batch_size:
                            # Обернем синхронную операцию в sync_to_async
                            await sync_to_async(LogEntry.objects.bulk_create)(log_entries)
                            log_entries.clear()
            if log_entries:
                await sync_to_async(LogEntry.objects.bulk_create)(log_entries)