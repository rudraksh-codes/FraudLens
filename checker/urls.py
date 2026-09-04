from django.urls import path
from . import views

urlpatterns = [
    path('', views.checker, name = "checker")
]