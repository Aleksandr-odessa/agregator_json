from django.contrib import admin
from .models import LogEntry


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'timestamp', 'http_method', 'uri', 'response_code', 'response_size')
    search_fields = ('ip_address', 'uri')
    list_filter = ('http_method', 'response_code')