from django.db import models
from django.utils import timezone
from datetime import timedelta

class Feeds(models.Model):
    nickname = models.CharField(max_length=6)
    content = models.CharField(max_length=300)
    created_at = models.DateTimeField(blank=True, editable=False)
    expires_at = models.DateTimeField(blank=True, editable=False)
    fan_cnt = models.PositiveIntegerField(default=0)
    wood_cnt = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["expires_at"]),
        ]

    def save(self, *args, **kwargs):
        now = timezone.now()
        if not self.created_at:
            self.created_at = now
            self.expires_at = now + timedelta(hours=24)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nickname} ({self.created_at}): {self.content[:20]}..."


class Comments(models.Model):
    nickname = models.CharField(max_length=6)
    content = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    feed = models.ForeignKey(Feeds, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"self.feed - self.nickname ({self.created_at}): {self.content[:20]}..."