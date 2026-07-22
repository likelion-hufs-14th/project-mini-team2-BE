from django.db import models
from django.db.models import F
from django.db.models.functions import Least
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

    def add_reaction(self, reaction_type):
        max_expires_at = self.created_at + timedelta(hours=48)

        if reaction_type == 'fan':
            Feeds.objects.filter(pk=self.pk).update(
                fan_cnt=F('fan_cnt') + 1,
                expires_at=Least(F('expires_at') + timedelta(hours=1), max_expires_at)
            )
        elif reaction_type == 'wood':
            Feeds.objects.filter(pk=self.pk).update(
                wood_cnt=F('wood_cnt') + 1,
                expires_at=F('expires_at') - timedelta(minutes=10)
            )
        else:
            raise ValueError("잘못된 요청입니다.")
        
        self.refresh_from_db()

    def __str__(self):
        return f"{self.nickname} ({self.created_at}): {self.content[:20]}..."


class Comments(models.Model):
    nickname = models.CharField(max_length=6)
    content = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    feed = models.ForeignKey(Feeds, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        ordering = ["created_at"]
    
    def __str__(self):
        return f"{self.feed} - {self.nickname} ({self.created_at}): {self.content[:20]}..."
    

class BurnCount(models.Model):
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Burn Count: {self.count}"
    
    @classmethod
    def increment(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        cls.objects.filter(pk=1).update(count=F('count') + 1)
        obj.refresh_from_db()
        return obj