from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import User

from timetable.models import Timing, Professor, Year, Subject, Group


from .serializers import (
    TimingSerializer, ProfessorSerializer,
    YearSerializer,
    SubjectSerializer
)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getRoutes(request):

    routes = [
        {"GET", "/api/v1/"},
        {"GET", "/api/v1/rooms"},
    ]

    return Response(routes)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def timingView(request):
    user = request.user
    if request.method == 'GET':
        instance = user.timing_set.all()
        serializer = TimingSerializer(instance, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        instance = Timing.objects.create(day=data['day'])
        instance.start_time = data['start_time']
        instance.end_time = data['end_time']
        instance.skip_start_time = data['skip_start_time']
        instance.skip_end_time = data['skip_end_time']
        instance.one_slot_interval = data['one_slot_interval']
        instance.owner = user
        instance.save()
        return Response({"message": "Timing added successfully."})
    elif request.method == 'PUT':
        data = request.data
        instance = user.timing_set.get(id=data['id'])
        if 'day' in data:
            instance.day = data['day']
        if 'start_time' in data:
            instance.start_time = data['start_time']
        if 'end_time' in data:
            instance.end_time = data['end_time']
        if 'skip_start_time' in data:
            instance.skip_start_time = data['skip_start_time']
        if 'skip_end_time' in data:
            instance.skip_end_time = data['skip_end_time']
        if 'one_slot_interval' in data:
            instance.one_slot_interval = data['one_slot_interval']
        instance.save()
        return Response({"message": "Timing Updated successfully."})
    elif request.method == 'DELETE':
        instance = user.timing_set.get(id=request.data['id'])
        instance.delete()
        return Response({"message": "Timing deleted successfully."})


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def yearView(request):
    user = request.user
    if request.method == 'GET':
        instance = user.year_set.all()
        serializer = YearSerializer(instance, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        instance = Year.objects.create(semester=int(data['semester']))
        instance.room = data['room']
        instance.total_groups = data['total_groups']
        instance.owner = user
        instance.save()
        return Response({"message": "Year added successfully."})
    elif request.method == 'PUT':
        data = request.data
        instance = user.year_set.get(id=data['id'])
        if 'semester' in data:
            instance.semester = int(data['semester'])
        if 'room' in data:
            instance.room = data['room']
        if 'total_groups' in data:
            instance.total_groups = data['total_groups']
        instance.save()
        return Response({"message": "Year Updated successfully."})
    elif request.method == 'DELETE':
        instance = user.year_set.get(id=request.data['id'])
        instance.delete()
        return Response({"message": "Year deleted successfully."})


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def professorView(request):
    user = request.user
    if request.method == 'GET':
        instance = user.professor_set.all()
        serializer = ProfessorSerializer(instance, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        instance = Professor.objects.create(nick_name=data['nick_name'])
        instance.name = data['name']
        instance.owner = user
        instance.save()
        return Response({"message": "Professor added successfully."})
    elif request.method == 'PUT':
        data = request.data
        instance = user.professor_set.get(id=data['id'])
        if 'name' in data:
            instance.name = data['name']
        if 'nick_name' in data:
            instance.nick_name = data['nick_name']
        instance.save()
        return Response({"message": "Professor Updated successfully."})
    elif request.method == 'DELETE':
        instance = user.professor_set.get(id=request.data['id'])
        instance.delete()
        return Response({"message": "Professor deleted successfully."})


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def subjectView(request):
    user = request.user
    if request.method == 'GET':
        instance = user.subject_set.all()
        serializer = SubjectSerializer(instance=instance, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        instance = Subject.objects.create(code=data['code'], name=data['name'])
        teacher = user.professor_set.get(id=data['teacher_id'])
        instance.teacher = teacher
        year = user.year_set.get(id=data['year_id'])
        instance.year = year
        instance.owner = user
        for group in data['groups']:
            new_group = Group.objects.create(
                owner=user, group_number=group['group_number'],
                lecture_in_a_week=group['lecture_in_a_week'],
                slot_required=group['slot_required'], subject=instance)
            new_group.save()
        instance.save()
        return Response({"message": "Subject added successfully."})
    elif request.method == 'PUT':
        data = request.data
        instance = user.subject_set.get(id=data['id'])
        if 'name' in data:
            instance.name = data['name']
        if 'code' in data:
            instance.code = data['code']
        if 'teacher_id' in data:
            teacher = user.professor_set.get(id=data['teacher_id'])
            instance.teacher = teacher
        if 'year_id' in data:
            year = user.year_set.get(id=data['year_id'])
            instance.year = year
        instance.save()
        if 'groups' in data:
            for group in data['groups']:
                if 'id' in group:
                    grp = Group.objects.get(id=group['id'])
                    grp.lecture_in_a_week = group['lecture_in_a_week']
                    grp.slot_required = group['slot_required']
                    grp.group_number = group['group_number']
                    grp.save()
                else:
                    grp = Group.objects.create(
                        owner=user, group_number=group['group_number'],
                        lecture_in_a_week=group['lecture_in_a_week'],
                        slot_required=group['slot_required'],
                        subject=instance)
                    grp.save()
        return Response({"message": "Subject Updated successfully."})
    elif request.method == 'DELETE':
        instance = user.subject_set.get(id=request.data['id'])
        instance.delete()
        return Response({"message": "Subject deleted successfully."})


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


# @api_view(['GET'])
# def generateTimeTableView(request):
#     schedule = timetable(request)
#     sections = SectionSerializer(Section.objects.all(), many=True).data
#     return Response({"schedule": schedule, "sections": sections})
