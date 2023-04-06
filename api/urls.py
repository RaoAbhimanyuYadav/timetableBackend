from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from . import views


urlpatterns = [
    path("register/", views.register, name='register'),

    path("belltiming/", views.bellTimingView, name='belltiming'),
    path("workingday/", views.workingDayView, name='workingday'),
    path("timeoff/", views.timeOffView, name='timeoff'),
    path("subject/", views.subjectView, name='subject'),
    path("classroom/", views.classroomView, name='classroom'),
    path("semester/", views.semesterView, name='semester'),
    path("group/", views.groupView, name='group'),
    path("teacher/", views.teacherView, name='teacher'),
    path("lesson/", views.lessonView, name='lesson'),
    path("all/", views.allView, name='all'),

    path('login/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('login/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
