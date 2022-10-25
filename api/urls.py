from django.urls import path
from . import views

urlpatterns = [
    path("", views.getRoutes, name='routes'),
    path("room/", views.room, name='room'),

]
