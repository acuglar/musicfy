from django.urls import path
from accounts.views import UserView, LoginView


urlpatterns =[
    path('register', UserView.as_view()),
    path('login', LoginView.as_view()),
]