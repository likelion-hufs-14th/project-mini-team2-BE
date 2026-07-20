from rest_framework import serializers
from .models import Feeds, Comments, BurnCount
from drf_spectacular.utils import extend_schema_field

# Feeds
## Read (List, Detail)
class FeedSerializer(serializers.ModelSerializer):
    feed_id = serializers.IntegerField(source='id', read_only=True)
    comment_cnt = serializers.SerializerMethodField()

    class Meta:
        model = Feeds
        fields = ['feed_id', 'content', 'nickname', 'created_at', 'expires_at', 'fan_cnt', 'wood_cnt', 'comment_cnt']
    
    @extend_schema_field(serializers.IntegerField)
    def get_comment_cnt(self, obj):
        if hasattr(obj, 'comment_cnt'):
            return obj.comment_cnt
        return obj.comments.count()

## Create
class FeedCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feeds
        fields = ['content', 'nickname']

# Comments
## Read
class CommentListSerializer(serializers.ModelSerializer):
    cmt_id = serializers.IntegerField(source='id', read_only=True)
    feed_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Comments
        fields = ['cmt_id', 'feed_id', 'content', 'nickname', 'created_at']

## Create
class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['content', 'nickname']

# Burn Count
class BurnCountSerializer(serializers.ModelSerializer):
    burn_cnt = serializers.IntegerField(source='count', read_only=True)

    class Meta:
        model = BurnCount
        fields = ['burn_cnt']