from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.utils import timezone
from datetime import timedelta

from .models import Feeds
from .serializers import FeedListSerializer, FeedDetailSerializer, CommentListSerializer

# Burn Count
class BurnCountView(APIView):
    def post(self, request):
        now = timezone.now()
        Feeds.objects.create(created_at=now, expires_at=now + timedelta(seconds=10))
        return Response(status=status.HTTP_201_CREATED)

# Feed
class FeedListView(APIView):
    def get(self, request):
        feed = Feeds.objects.filter(expires_at__gt=timezone.now())
        serializer = FeedListSerializer(feed, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = FeedListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class FeedDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Feeds.objects.filter(expires_at__gt=timezone.now()), pk=pk)

    def get(self, request, pk):
        feed = self.get_object(pk)
        serializer = FeedDetailSerializer(feed)
        return Response(serializer.data)


# Comment
class CommentListView(APIView):
    def get_feed(self, pk):
        return get_object_or_404(Feeds.objects.filter(expires_at__gt=timezone.now()), pk=pk)


    def get(self, request, pk):
        feed = self.get_feed(pk)
        comments = feed.comments.all()
        serializer = CommentListSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        feed = self.get_feed(pk)
        serializer = CommentListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(feed=feed)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FeedReactionView(APIView):
    def post(self, request, pk, reaction_type):
        feed = get_object_or_404(Feeds, pk=pk)

        if reaction_type == 'fan':
            feed.fan_cnt += 1
        elif reaction_type == 'wood':
            feed.wood_cnt += 1
        else:
            return Response(
                {"error": "잘못된 요청입니다."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        feed.save()

        return Response({
            "feed_id": feed.id,
            "fan_cnt": feed.fan_cnt,
            "wood_cnt": feed.wood_cnt
        }, status=status.HTTP_200_OK)