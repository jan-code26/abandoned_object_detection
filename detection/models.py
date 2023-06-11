from django.db import models

class DetectionResult(models.Model):
    video = models.FileField(upload_to='videos/')
    results = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class DetectionVideo(models.Model):
    # Add your fields and attributes here
    name = models.CharField(max_length=100)
    video_file = models.FileField(upload_to='videos/')

# class Video(models.Model):
#     file = models.FileField(upload_to='videos/')