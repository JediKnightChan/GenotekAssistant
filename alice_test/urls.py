from django.urls import path
from . import views

urlpatterns = [
    path('', views.alice_test, name='alice_test'),
]