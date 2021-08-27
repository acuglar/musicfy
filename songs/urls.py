from django import urls
from django.urls import path
from .views import SampleView, ParamView

urlpatterns = [
    path('sample/', SampleView.as_view()),
    path('sample/<str:name>/', ParamView.as_view()),
]