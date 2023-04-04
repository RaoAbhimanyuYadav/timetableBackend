from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import User

from timetable.models import Bell_Timing, Working_Day, Subject, Classroom, Semester


from .serializers import (
    BellTimingSerializer,
    WorkingDaySerializer,
    TimeOffSerializer,
    SubjectSerializer,
    ClassroomSerializer,
    # SemesterSerializer,
    # TeacherSerializer,
    # LessonSerializer,
    # LessonFormatSerializer
)

from .functions import (get_handler, set_handler,
                        delete_handler, update_handler, create_handler)


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
        return get_handler(
            user.bell_timing_set, BellTimingSerializer, 'Bell Timing'
        )
    if request.method == 'POST':
        return create_handler(request, BellTimingSerializer, "Start and End Time must be unique")
    if request.method == 'DELETE':
        return delete_handler(
            user.bell_timing_set, request, 'Bell Timing'
        )
    if request.method == 'PUT':
        return update_handler(
            request, user.bell_timing_set,
            BellTimingSerializer, Bell_Timing
        )


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def workingDayView(request):
    user = request.user
    if request.method == 'GET':
        return get_handler(
            user.working_day_set, WorkingDaySerializer, "Working Day"
        )
    if request.method == 'POST':
        return create_handler(request, WorkingDaySerializer, "Day must be unique")
    if request.method == 'DELETE':
        return delete_handler(
            user.working_day_set, request, 'Working Day'
        )
    if request.method == 'PUT':
        return update_handler(
            request, user.working_day_set,
            WorkingDaySerializer, Working_Day
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def timeOffView(request):
    user = request.user
    if request.method == 'GET':
        return get_handler(
            user.time_off_set, TimeOffSerializer, "Time Off"
        )


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def subjectView(request):
    user = request.user
    if request.method == 'GET':
        return get_handler(
            user.subject_set, SubjectSerializer, "Subject"
        )
    if request.method == 'POST':
        return create_handler(
            request, SubjectSerializer, "Subject Code must be unique",
            time_off=request.data.get('time_off', [])
        )
    if request.method == 'DELETE':
        return delete_handler(
            user.subject_set, request, 'Subject'
        )
    if request.method == 'PUT':
        return update_handler(
            request, user.subject_set,
            SubjectSerializer, Subject,
            time_off=request.data.get('time_off', [])
        )


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def classroomView(request):
    user = request.user
    if request.method == 'GET':
        return get_handler(
            user.classroom_set, ClassroomSerializer, "Classroom"
        )
    if request.method == 'POST':
        return create_handler(
            request, ClassroomSerializer, "Classroom Code must be unique",
            time_off=request.data.get('time_off', [])
        )
    if request.method == 'DELETE':
        return delete_handler(
            user.classroom_set, request, 'Classroom'
        )
    if request.method == 'PUT':
        return update_handler(
            request, user.classroom_set,
            ClassroomSerializer, Classroom,
            time_off=request.data.get('time_off', [])
        )

# @api_view(['GET', 'POST', 'PUT', 'DELETE'])
# @permission_classes([IsAuthenticated])
# def semesterView(request):
#     user = request.user
#     if request.method == 'GET':
#         return get_handler(
#             user.semester_set, SemesterSerializer, "Semester"
#         )
#     if request.method == 'POST':
#         return create_handler(
#             request, SemesterSerializer, "Semester Code must be unique",
#             time_off=request.data.get('time_off', [])
#         )
#     if request.method == 'DELETE':
#         return delete_handler(
#             user.semester_set, request, 'Semester'
#         )
#     if request.method == 'PUT':
#         return update_handler(
#             request, user.semester_set,
#             SemesterSerializer, Semester, time_off=request.data.get('time_off', [])
#         )


# @api_view(['GET', 'POST', 'PUT', 'DELETE'])
# @permission_classes([IsAuthenticated])
# def teacherView(request):
#     user = request.user
#     if request.method == 'GET':
#         return Response(
#             get_handler(
#                 user.teacher_set, TeacherSerializer, 'Teacher'
#             ))
#     if request.method == 'POST':
#         return Response({
#             "message": "Teacher added successfully.",
#             "data": TeacherSerializer().create(request.data, user)
#         })
#     if request.method == 'DELETE':
#         return Response(
#             delete_handler(
#                 user.teacher_set, request, 'Teacher'
#             ))
#     if request.method == 'PUT':
#         instance = user.teacher_set.get(id=request.data['id'])
#         return Response({
#             "message": "Teacher Updated successfully.",
#             "data": TeacherSerializer().update(instance, request.data, user)
#         })


# @api_view(['GET', 'POST', 'PUT', 'DELETE'])
# @permission_classes([IsAuthenticated])
# def lessonView(request):
#     user = request.user
#     if request.method == 'GET':
#         inst = user.lesson_set.all()
#         if request.query_params:
#             inst = user.lesson_set.filter(teacher=request.query_params['id'])
#             return Response({"data": LessonSerializer(inst, many=True).data})
#         return Response({"data": LessonFormatSerializer(inst, many=True).data})

#     if request.method == 'POST':
#         return Response({
#             "message": "Lesson added successfully.",
#             "data": LessonSerializer().create(request.data, user)
#         })
#     if request.method == 'DELETE':
#         return Response(
#             delete_handler(
#                 user.lesson_set, request, 'Lesson'
#             ))
#     if request.method == 'PUT':
#         instance = user.lesson_set.get(id=request.data['id'])
#         return Response({
#             "message": "Lesson Updated successfully.",
#             "data": LessonSerializer().update(instance, request.data, user)
#         })


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def allView(request):
#     user = request.user
#     if request.method == 'GET':
#         resp = {
#             'bellTiming': get_handler(
#                 user.bell_timing_set, BellTimingSerializer, 'Bell Timing'
#             )['data'],
#             'workingDay': get_handler(
#                 user.working_day_set, WorkingDaySerializer, "Working Day"
#             )['data'],
#             'subject': get_handler(
#                 user.subject_set, SubjectSerializer, "Subject"
#             )['data'],
#             'semester': get_handler(
#                 user.semester_set, SemesterSerializer, 'Semester'
#             )['data'],
#             'classroom': get_handler(
#                 user.classroom_set, ClassroomSerializer, "Classroom"
#             )['data'],
#             'teacher': get_handler(
#                 user.teacher_set, TeacherSerializer, 'Teacher'
#             )['data']
#         }

#         return Response(resp)
