from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views


urlpatterns = [
    path("", views.getRoutes, name='routes'),
    path("room/", views.roomView, name='room'),
    path("instructor/", views.instructorView, name='instructor'),
    path("meeting-time/", views.meetingTimeView, name='meeting-time'),
    path("course/", views.courseView, name='course'),
    path("department/", views.departmentView, name='department'),
    path("section/", views.sectionView, name='section'),

    path('user/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
