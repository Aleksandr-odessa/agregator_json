from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LogEntryViewSet, index, download_file

router = DefaultRouter()
router.register(r'logsjs', LogEntryViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', index, name='home'),
    path('download/',download_file, name='download')
]