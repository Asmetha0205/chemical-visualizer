from django.db import models

class UploadHistory(models.Model):
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    total_records = models.IntegerField()
    avg_flowrate = models.FloatField()
    avg_pressure = models.FloatField()
    avg_temperature = models.FloatField()

    type_distribution = models.JSONField()  # Stores dict as JSON

    def __str__(self):
        return f"{self.filename} - {self.uploaded_at}"
