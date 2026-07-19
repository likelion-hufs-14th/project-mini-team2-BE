from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Feeds

class FeedReactionView(APIView):
    def post(self, request, pk, reaction_type):
        feed = get_object_or_404(Feeds, pk=pk)

        try:
            feed.add_reaction(reaction_type)
        except ValueError as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({
            "feed_id": feed.id,
            "fan_cnt": feed.fan_cnt,
            "wood_cnt": feed.wood_cnt,
            "expires_at": feed.expires_at
        }, status=status.HTTP_200_OK)