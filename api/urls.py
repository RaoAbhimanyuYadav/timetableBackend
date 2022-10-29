from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views


urlpatterns = [
    path("", views.getRoutes, name='routes'),
    path("register/", views.register, name='register'),
    path("timing/", views.timingView, name='timing'),
    path("year/", views.yearView, name='year'),
    # path("meeting-time/", views.meetingTimeView, name='meeting-time'),
    # path("course/", views.courseView, name='course'),
    # path("department/", views.departmentView, name='department'),
    # path("section/", views.sectionView, name='section'),
    # path("generate-timetable/", views.generateTimeTableView,
    #      name='generate-timetable'),

    path('login/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
