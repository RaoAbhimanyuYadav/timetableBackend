from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from . import views


urlpatterns = [
    # path("", views.getRoutes, name='routes'),
    path("register/", views.register, name='register'),

    path("belltiming/", views.bellTimingView, name='belltiming'),
    path("workingday/", views.workingDayView, name='workingday'),
    path("subject/", views.subjectView, name='subject'),
    path("semester/", views.semesterView, name='semester'),
    path("classroom/", views.classroomView, name='classroom'),
    path("teacher/", views.teacherView, name='teacher'),

    path('login/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('login/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
