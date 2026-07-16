from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Feeds

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