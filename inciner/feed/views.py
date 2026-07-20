from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse, inline_serializer
from rest_framework import serializers

from .models import Feeds, BurnCount
from .serializers import FeedSerializer, FeedCreateSerializer, CommentListSerializer, CommentCreateSerializer, BurnCountSerializer

# Burn Count
class BurnCountView(APIView):
    @extend_schema(
        request=None,
        responses={
            201: OpenApiResponse(response=BurnCountSerializer, description="Created"),
        }
    )
    def post(self, request):
        burn = BurnCount.increment()
        serializer = BurnCountSerializer(burn)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        responses={
            200: OpenApiResponse(response=BurnCountSerializer, description="OK"),
        }
    )
    def get(self, request):
        burn, _ = BurnCount.objects.get_or_create(pk=1)
        serializer = BurnCountSerializer(burn)
        return Response(serializer.data)

# Feed
class FeedListView(APIView):
    @extend_schema(
        responses={
            200: OpenApiResponse(response=FeedSerializer(many=True), description="OK"),
        }
    )
    def get(self, request):
        feed = Feeds.objects.filter(expires_at__gt=timezone.now()).annotate(
            comment_cnt=Count('comments')
        )
        serializer = FeedSerializer(feed, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=FeedCreateSerializer,
        responses={
            201: OpenApiResponse(response=FeedSerializer, description="Created"),
            400: OpenApiResponse(description="Bad Request"),
        },
    )
    def post(self, request):
        serializer = FeedCreateSerializer(data=request.data)
        if serializer.is_valid():
            feed = serializer.save()
            return Response(FeedSerializer(feed).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class FeedDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Feeds.objects.filter(expires_at__gt=timezone.now()), pk=pk)

    @extend_schema(
        responses={
            200: OpenApiResponse(response=FeedSerializer, description="OK"),
            404: OpenApiResponse(description="Not Found"),
        }
    )
    def get(self, request, pk):
        feed = self.get_object(pk)
        serializer = FeedSerializer(feed)
        return Response(serializer.data)


# Comment
class CommentListView(APIView):
    def get_feed(self, pk):
        return get_object_or_404(Feeds.objects.filter(expires_at__gt=timezone.now()), pk=pk)

    @extend_schema(
        responses={
            200: OpenApiResponse(response=CommentListSerializer(many=True), description="OK"),
            404: OpenApiResponse(description="Not Found"),
        }
    )
    def get(self, request, pk):
        feed = self.get_feed(pk)
        comments = feed.comments.all()
        serializer = CommentListSerializer(comments, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=CommentCreateSerializer,
        responses={
            201: OpenApiResponse(response=CommentListSerializer, description="Created"),
            400: OpenApiResponse(description="Bad Request"),
            404: OpenApiResponse(description="Not Found"),
        },
    )
    def post(self, request, pk):
        feed = self.get_feed(pk)
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save(feed=feed)
            return Response(CommentListSerializer(comment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Reaction
class FeedReactionView(APIView):
    @extend_schema(
        request=FeedSerializer,
        responses={
            201: OpenApiResponse(response=FeedSerializer, description="Created"),
            404: OpenApiResponse(description="Not Found"),
        },
    )

    def post(self, request, pk, reaction_type):
        feed = get_object_or_404(Feeds, pk=pk)

        try:
            feed.add_reaction(reaction_type)
        except ValueError as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(FeedSerializer(feed).data, status=status.HTTP_200_OK)