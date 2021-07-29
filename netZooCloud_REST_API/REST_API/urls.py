from django.urls import path
from . import views


urlpatterns = [
    path("lioness", views.lioness, name = "lioness")
]