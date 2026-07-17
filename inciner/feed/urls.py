from django.urls import path
from .views import FeedListView, FeedDetailView, CommentListView, BurnCountView

urlpatterns = [
    path('', FeedListView.as_view()),
    path('<int:pk>/', FeedDetailView.as_view()),
    path('<int:pk>/comments/', CommentListView.as_view()),
    path('burn/', BurnCountView.as_view()),
]