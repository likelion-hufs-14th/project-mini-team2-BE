from django.urls import path
from .views import FeedListView, FeedDetailView, CommentListView, FeedReactionView, BurnCountView

urlpatterns = [
    path('', FeedListView.as_view()),
    path('<int:pk>/', FeedDetailView.as_view()),
    path('<int:pk>/comments/', CommentListView.as_view()),
    path('burn/', BurnCountView.as_view()),
    path('<int:pk>/react/<str:reaction_type>/', FeedReactionView.as_view(), name='feed-react'),
]