from django.db import models

class LogEntry(models.Model):
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField()
    http_method = models.CharField(max_length=10)
    uri = models.CharField(max_length=300)
    response_code = models.IntegerField()
    response_size = models.IntegerField()

    def __str__(self):
        return f"{self.ip_address} - {self.http_method} - {self.uri}-{self.response_code}"

