from django.urls import path
from .views import FeedListView, FeedDetailView, CommentListView, FeedReactionView, BurnCountView

urlpatterns = [
    path('', FeedListView.as_view()),
    path('<int:feed_id>/', FeedDetailView.as_view()),
    path('<int:feed_id>/comments/', CommentListView.as_view()),
    path('burn/', BurnCountView.as_view()),
    path('<int:feed_id>/react/<str:reaction_type>/', FeedReactionView.as_view(), name='feed-react'),
]