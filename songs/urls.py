from django.urls import path
from .views import SampleView, ParamView, MusicfyArtistView, MusicfySongView

urlpatterns = [
    path('sample/', SampleView.as_view()),
    path('sample/<str:name>/', ParamView.as_view()),
    path('musicfy/', MusicfyArtistView.as_view()),
    path('musicfy/songs/', MusicfySongView.as_view()),
]