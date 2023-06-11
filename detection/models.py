from django.db import models

class DetectionResult(models.Model):
    video = models.FileField(upload_to='videos/')
    results = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.created_at)
