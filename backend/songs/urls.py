from django.urls import path
from .views import SongListView, SongDetailView, ScoreDownloadView

urlpatterns = [
    path('', SongListView.as_view(), name='song-list'),
    path('<int:pk>/', SongDetailView.as_view(), name='song-detail'),
    path('<int:pk>/score/', ScoreDownloadView.as_view(), name='score-download'),
]
