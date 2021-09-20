from django.urls import path
from .views import SampleView, ArtistView, ArtistDetailView, PlaylistView, PlaylistDetailView

urlpatterns = [
    path('sample/', SampleView.as_view()),
    path('artists/', ArtistView.as_view()),
    path('artists/<int:artist_id>', ArtistDetailView.as_view()),
    path('playlists/', PlaylistView.as_view()),
    path('playlists/<int:playlist_id>/', PlaylistDetailView.as_view())
]