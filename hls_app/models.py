from django.db import models
from django.utils import timezone


class Video(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Добавляем дату загрузки

    def __str__(self):
        return self.title
