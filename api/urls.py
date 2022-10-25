from django.urls import path
from . import views

urlpatterns = [
    path("", views.getRoutes, name='routes'),
    path("room/", views.roomView, name='room'),
    path("instructor/", views.instructorView, name='instructor'),
    path("meeting-time/", views.meetingTimeView, name='meeting-time'),

]
