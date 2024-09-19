from django.http import HttpResponse, FileResponse
from rest_framework import viewsets, filters
from .models import LogEntry
from .serializers import LogEntrySerializer
from rest_framework.pagination import PageNumberPagination

class LogEntryPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000

class LogEntryViewSet(viewsets.ModelViewSet):
    queryset = LogEntry.objects.all()  # Получение всех записей из таблицы LogEntry
    serializer_class = LogEntrySerializer  # Указание сериализатора для работы с данными
    pagination_class = LogEntryPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['ip_address', 'uri']
    ordering_fields = ['timestamp', 'response_code']

def index(request):
    return HttpResponse("Hello Django")

def download_file(request):
    return FileResponse(open("logs.txt", "rb"))