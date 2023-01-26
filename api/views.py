from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import User

from timetable.models import (
    Bell_Timing, Working_Day, Lesson,
    Subject, Subject_Time_Off,
    Semester, Semester_Group, Semester_Time_Off,
    Classroom, Classroom_Time_Off,
    Teacher, Teacher_Time_Off, )

from .serializers import (
    BellTimingSerializer,
    WorkingDaySerializer,
    SubjectSerializer,
    SemesterSerializer,
    ClassroomSerializer,
    TeacherSerializer
)

from .functions import get_handler, set_handler, delete_handler


# from rest_framework.permissions import  IsAdminUser
# @permission_classes([IsAdminUser])


@api_view(['POST'])
def register(request):
    data = request.data
    username = data['username'].lower()
    try:
        instance = User.objects.get(username=username)
        return Response({"message": "User with this username already exists."})
    except User.DoesNotExist:
        instance = User.objects.create(
            username=username,
            password=data['password']
        )
        if 'email' in data:
            instance.email = data['email']
        if 'first_name' in data:
            instance.first_name = data['first_name']
        if 'last_name' in data:
            instance.last_name = data['last_name']
        instance.save()
        refresh = RefreshToken.for_user(instance)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def bellTimingView(request):
    user = request.user
    if request.method == 'GET':
        return Response(
            get_handler(
                user.bell_timing_set, BellTimingSerializer, 'Bell Timing'
            ))
    if request.method == 'POST':
        return Response(
            set_handler(
                Bell_Timing, user, request.data,
                ['name', 'start_time', 'end_time'],
                BellTimingSerializer, 'Bell Timing'
            ))
    if request.method == 'DELETE':
        return Response(
            delete_handler(
                user.bell_timing_set, request, 'Bell Timing'
            ))
    # elif request.method == 'PUT':
    #     data = request.data
    #     instance = user.timing_set.get(id=data['id'])
    #     if 'day' in data:
    #         instance.day = data['day']
    #     if 'start_time' in data:
    #         instance.start_time = data['start_time']
    #     if 'end_time' in data:
    #         instance.end_time = data['end_time']
    #     if 'skip_start_time' in data:
    #         instance.skip_start_time = data['skip_start_time']
    #     if 'skip_end_time' in data:
    #         instance.skip_end_time = data['skip_end_time']
    #     if 'one_slot_interval' in data:
    #         instance.one_slot_interval = data['one_slot_interval']
    #     instance.save()
    #     return Response({"message": "Timing Updated successfully."})


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def workingDayView(request):
    user = request.user
    if request.method == 'GET':
        return Response(
            get_handler(
                user.working_day_set, WorkingDaySerializer, "Working Day"
            ))
    if request.method == 'POST':
        return Response(
            set_handler(
                Working_Day, user, request.data,
                ['name', 'code'],
                WorkingDaySerializer, "Working Day"
            ))
    if request.method == 'DELETE':
        return Response(
            delete_handler(
                user.working_day_set, request, 'Working Day'
            ))


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def subjectView(request):
    user = request.user
    if request.method == 'GET':
        return Response(
            get_handler(
                user.subject_set, SubjectSerializer, "Subject"
            ))
    if request.method == 'POST':
        return Response({
            "message": "Subject added successfully.",
            "data": SubjectSerializer().create(request.data, user)
        })
    if request.method == 'DELETE':
        return Response(
            delete_handler(
                user.subject_set, request, 'Subject'
            ))


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def semesterView(request):
    user = request.user
    if request.method == 'GET':
        return Response(
            get_handler(
                user.semester_set, SemesterSerializer, 'Semester'
            ))
    if request.method == 'POST':
        return Response({
            "message": "Semester added successfully.",
            "data": SemesterSerializer().create(request.data, user)
        })
    if request.method == 'DELETE':
        return Response(
            delete_handler(
                user.semester_set, request, 'Semester'
            ))


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def classroomView(request):
    user = request.user
    if request.method == 'GET':
        return Response(
            get_handler(
                user.classroom_set, ClassroomSerializer, "Classroom"
            ))
    if request.method == 'POST':
        return Response({
            "message": "Classroom added successfully.",
            "data": ClassroomSerializer().create(request.data, user)
        })
    if request.method == 'DELETE':
        return Response(
            delete_handler(
                user.classroom_set, request, 'Classroom'
            ))


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def teacherView(request):
    user = request.user
    if request.method == 'GET':
        return Response(
            get_handler(
                user.teacher_set, TeacherSerializer, 'Teacher'
            ))
    if request.method == 'POST':
        return Response({
            "message": "Teacher added successfully.",
            "data": TeacherSerializer().create(request.data, user)
        })
    if request.method == 'DELETE':
        return Response(
            delete_handler(
                user.teacher_set, request, 'Teacher'
            ))
