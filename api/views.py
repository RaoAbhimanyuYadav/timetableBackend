from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import User

from timetable.models import Bell_Timing, Working_Day

from .serializers import (
    BellTimingSerializer,
    WorkingDaySerializer,
    SubjectSerializer,
    SemesterSerializer,
    ClassroomSerializer,
    TeacherSerializer,
    LessonSerializer,
    LessonFormatSerializer
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
        instance.set_password(data['password'])
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
    if request.method == 'PUT':
        instance = user.bell_timing_set.get(id=request.data['id'])
        return Response({
            "message": "Bell Timing Updated successfully.",
            "data": BellTimingSerializer().update(instance, request.data)
        })


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
    if request.method == 'PUT':
        instance = user.working_day_set.get(id=request.data['id'])
        return Response({
            "message": "Working Day Updated successfully.",
            "data": WorkingDaySerializer().update(instance, request.data)
        })


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
    if request.method == 'PUT':
        instance = user.subject_set.get(id=request.data['id'])
        return Response({
            "message": "Subject Updated successfully.",
            "data": SubjectSerializer().update(instance, request.data, user)
        })


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
    if request.method == 'PUT':
        instance = user.semester_set.get(id=request.data['id'])
        return Response({
            "message": "Semester Updated successfully.",
            "data": SemesterSerializer().update(instance, request.data, user)
        })


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
    if request.method == 'PUT':
        instance = user.classroom_set.get(id=request.data['id'])
        return Response({
            "message": "Classroom Updated successfully.",
            "data": ClassroomSerializer().update(instance, request.data, user)
        })


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
    if request.method == 'PUT':
        instance = user.teacher_set.get(id=request.data['id'])
        return Response({
            "message": "Teacher Updated successfully.",
            "data": TeacherSerializer().update(instance, request.data, user)
        })


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def lessonView(request):
    user = request.user
    if request.method == 'GET':
        inst = user.lesson_set.all()
        if request.query_params:
            inst = user.lesson_set.filter(teacher=request.query_params['id'])
            return Response({"data": LessonSerializer(inst, many=True).data})
        return Response({"data": LessonFormatSerializer(inst, many=True).data})

    if request.method == 'POST':
        return Response({
            "message": "Lesson added successfully.",
            "data": LessonSerializer().create(request.data, user)
        })
    if request.method == 'DELETE':
        return Response(
            delete_handler(
                user.lesson_set, request, 'Lesson'
            ))
    if request.method == 'PUT':
        instance = user.lesson_set.get(id=request.data['id'])
        return Response({
            "message": "Lesson Updated successfully.",
            "data": LessonSerializer().update(instance, request.data, user)
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def allView(request):
    user = request.user
    if request.method == 'GET':
        resp = {
            'bellTiming': get_handler(
                user.bell_timing_set, BellTimingSerializer, 'Bell Timing'
            )['data'],
            'workingDay': get_handler(
                user.working_day_set, WorkingDaySerializer, "Working Day"
            )['data'],
            'subject': get_handler(
                user.subject_set, SubjectSerializer, "Subject"
            )['data'],
            'semester': get_handler(
                user.semester_set, SemesterSerializer, 'Semester'
            )['data'],
            'classroom': get_handler(
                user.classroom_set, ClassroomSerializer, "Classroom"
            )['data'],
            'teacher': get_handler(
                user.teacher_set, TeacherSerializer, 'Teacher'
            )['data']
        }

        return Response(resp)
