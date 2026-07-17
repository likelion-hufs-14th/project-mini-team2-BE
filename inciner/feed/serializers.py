from rest_framework import serializers
from .models import Feeds, Comments

class FeedListSerializer(serializers.ModelSerializer):
    feed_id = serializers.IntegerField(source='id', read_only=True)
    class Meta:
        model = Feeds
        fields = ['feed_id', 'content', 'nickname', 'created_at', 'expires_at', 'fan_cnt', 'wood_cnt']
        read_only_fields = ['created_at', 'expires_at', 'fan_cnt', 'wood_cnt']

class FeedDetailSerializer(serializers.ModelSerializer):
    feed_id = serializers.IntegerField(source='id', read_only=True)
    class Meta:
        model = Feeds
        fields = ['feed_id', 'content', 'nickname', 'created_at', 'expires_at', 'fan_cnt', 'wood_cnt']
        read_only_fields = ['created_at', 'expires_at', 'fan_cnt', 'wood_cnt']

class CommentListSerializer(serializers.ModelSerializer):
    cmt_id = serializers.IntegerField(source='id', read_only=True)
    class Meta:
        model = Comments
        fields = ['cmt_id', 'content', 'nickname', 'created_at']