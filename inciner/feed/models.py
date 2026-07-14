from django.db import models
from django.utils import timezone
from datetime import timedelta

class Feeds(models.Model):
    nickname = models.CharField(max_length=15)
    content = models.CharField(max_length=300)
    created_at = models.DateTimeField(editable=False)
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
    content = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"({self.created_at}): {self.content[:20]}..."
        # 닉네임 필요한데 Feeds 모델에 국한되어있음. 논의 후 수정 필요.