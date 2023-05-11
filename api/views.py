from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import User

from timetable.models import (
    Bell_Timing, Working_Day, Subject,
    Classroom, Semester, Group,
    Teacher, Lesson
)


from .serializers import (
    BellTimingSerializer,
    WorkingDaySerializer,
    GroupSerializer,
    TimeOffSerializer,
    SubjectSerializer,
    ClassroomSerializer,
    SemesterSerializer,
    TeacherSerializer,
    LessonSerializer,
    SavedTimetableSerializer,
    SavedWithoutDataTimetableSerializer
    # LessonFormatSerializer
)

from .functions import (
    get_handler, delete_handler,
    update_handler, create_handler)


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


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def groupView(request):
    user = request.user
    if request.method == 'GET':
        return get_handler(
            user.group_set, GroupSerializer, "Semester Group"
        )
    if request.method == 'POST':
        return create_handler(request, GroupSerializer, "Code must be unique")
    if request.method == 'DELETE':
        return delete_handler(
            user.group_set, request, 'Semester Group'
        )
    if request.method == 'PUT':
        return update_handler(
            request, user.group_set,
            GroupSerializer, Group
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


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def semesterView(request):
    user = request.user
    if request.method == 'GET':
        return get_handler(
            user.semester_set, SemesterSerializer, "Semester"
        )
    if request.method == 'POST' or request.method == "PUT":
        if 'classroom' in request.data:
            if request.data.get('groups', []).__len__() > 0:
                if request.method == "POST":
                    return create_handler(
                        request, SemesterSerializer, "Semester Code must be unique",
                        classroom=request.data['classroom'],
                        time_off=request.data.get('time_off', []),
                        groups=request.data['groups']
                    )
                if request.method == "PUT":
                    return update_handler(
                        request, user.semester_set,
                        SemesterSerializer, Semester,
                        classroom=request.data['classroom'],
                        time_off=request.data.get('time_off', []),
                        groups=request.data['groups']
                    )

            else:
                return Response(
                    status=400,
                    data={"message": "Please select at least 1 group"}
                )
        else:
            return Response(
                status=400,
                data={"message": "Please send classroom"}
            )
    if request.method == 'DELETE':
        return delete_handler(
            user.semester_set, request, 'Semester'
        )


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def teacherView(request):
    user = request.user
    if request.method == 'GET':
        return get_handler(
            user.teacher_set, TeacherSerializer, "Teacher"
        )
    if request.method == 'POST':
        return create_handler(
            request, TeacherSerializer, "Teacher Code must be unique",
            time_off=request.data.get('time_off', [])
        )
    if request.method == 'DELETE':
        return delete_handler(
            user.teacher_set, request, 'Teacher'
        )
    if request.method == 'PUT':
        return update_handler(
            request, user.teacher_set,
            TeacherSerializer, Teacher,
            time_off=request.data.get('time_off', [])
        )


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def lessonView(request):
    user = request.user
    if request.method == 'GET':
        inst = user.lesson_set.all()
        if request.query_params:
            inst = user.lesson_set.filter(teachers=request.query_params['id'])
            return Response(
                status=200,
                data={
                    "message": "Lessons fetched succesfully",
                    "data": LessonSerializer(inst, many=True).data
                }
            )
        else:
            return Response(
                status=200,
                data={
                    "message": "Lessons fetched succesfully",
                    "data": LessonSerializer(inst, many=True).data
                }
            )

    if request.method == 'POST':
        return create_handler(
            request, LessonSerializer, "It must be unique",
            classroom=request.data.get('classroom', {}),
            subject=request.data.get('subject', {}),
            sem_grps=request.data.get('sem_grps', [{}]),
            teachers=request.data.get('teachers', [{}]),
        )
    if request.method == 'DELETE':
        return delete_handler(
            user.lesson_set, request, 'Lesson'
        )
    if request.method == 'PUT':
        return update_handler(
            request, user.lesson_set,
            LessonSerializer, Lesson,
            classroom=request.data.get('classroom', {}),
            subject=request.data.get('subject', {}),
            sem_grps=request.data.get('sem_grps', [{}]),
            teachers=request.data.get('teachers', [{}]),
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def allView(request):
    user = request.user
    if request.method == 'GET':
        resp = {
            "message": "All data fetched successfully",
            'bellTiming': BellTimingSerializer(user.bell_timing_set.all(), many=True).data,
            'workingDay': WorkingDaySerializer(user.working_day_set.all(), many=True).data,
            'subject': SubjectSerializer(user.subject_set.all(), many=True).data,
            'semester': SemesterSerializer(user.semester_set.all(), many=True).data,
            'classroom':  ClassroomSerializer(user.classroom_set.all(), many=True).data,
            'teacher': TeacherSerializer(user.teacher_set.all(), many=True).data,
            "groups": GroupSerializer(user.group_set.all(), many=True).data,
            'timeOffs': TimeOffSerializer(user.time_off_set.all(), many=True).data
        }

        return Response(data=resp, status=200)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def savedTimetableView(request):
    user = request.user
    if request.method == 'GET':
        if request.query_params:
            inst = user.saved_timetable_set.filter(
                id=request.query_params['id'])
            return Response(
                status=200,
                data={
                    "message": "Saved Timetable fetched succesfully",
                    "data": SavedTimetableSerializer(inst, many=True).data
                }
            )
        else:
            inst = user.saved_timetable_set.all()
            return Response(
                status=200,
                data={
                    "message": "Saved Timetables fetched succesfully",
                    "data": SavedWithoutDataTimetableSerializer(inst, many=True).data
                }
            )

    if request.method == 'POST':
        return create_handler(
            request, SavedTimetableSerializer, "It must be unique",
        )
    if request.method == 'DELETE':
        return delete_handler(
            user.saved_timetable_set, request, 'Saved Timetable'
        )
