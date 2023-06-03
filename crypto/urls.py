from django.urls import path
from . import views

urlpatterns = [
    path('', views.CoinAPIView.as_view()),
]