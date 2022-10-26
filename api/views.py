from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .serializers import (
    RoomSerializer, InstructorSerializer, MeetingTimeSerializer, CourseSerializer,
    DepartmentSerializer, SectionSerializer
)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getRoutes(request):

    routes = [
        {"GET", "/api/v1/"},
        {"GET", "/api/v1/rooms"},
    ]

    return Response(routes)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def roomView(request):
    user = request.user
    if request.method == 'GET':
        rooms = user.room_set.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        room, created = user.room_set.get_or_create(r_number=data['r_number'])
        room.owner = user
        room.seating_capacity = data['seating_capacity']
        room.save()
        return Response({"message": f"Room {'added' if created else 'updated'} successfully."})
    elif request.method == 'DELETE':
        room = user.room_set.get(r_number=request.data['r_number'])
        room.delete()
        return Response({"message": "Room deleted successfully."})


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def instructorView(request):
    user = request.user
    if request.method == 'GET':
        instruc = user.instructor_set.all()
        serializer = InstructorSerializer(instruc, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        instruc, created = user.instructor_set.get_or_create(
            uid=data['uid'])
        instruc.owner = user
        instruc.name = data['name']
        instruc.save()
        return Response(
            {"message": f"Instructor {'added' if created else 'updated'} successfully."}
        )
    elif request.method == 'DELETE':
        instruc = user.instructor_set.get(uid=request.data['uid'])
        instruc.delete()
        return Response({"message": "Instructor deleted successfully."})


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def meetingTimeView(request):
    user = request.user
    if request.method == 'GET':
        instance = user.meetingtime_set.all()
        serializer = MeetingTimeSerializer(instance, many=True)
        return Response(serializer.data)
    elif request.method == 'POST' or 'PUT':
        data = request.data
        instance, created = user.meetingtime_set.get_or_create(
            pid=data['pid'])
        instance.owner = user
        instance.time = data['time']
        instance.day = data['day']
        instance.save()
        return Response(
            {"message": f"Meeting Time {'added' if created else 'updated'} successfully."}
        )
    elif request.method == 'DELETE':
        instance = user.meetingtime_set.get(pid=request.data['pid'])
        instance.delete()
        return Response({"message": "Meeting Time deleted successfully."})


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def courseView(request):
    user = request.user
    if request.method == 'GET':
        instance = user.course_set.all()
        serializer = CourseSerializer(instance, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        instance, created = user.course_set.get_or_create(
            course_number=data['course_number'])
        instance.owner = user
        instance.course_name = data['course_name']
        instance.max_numb_students = data['max_numb_students']
        for instructor_uid in data['instructor_uids']:
            instructor_obj = user.instructor_set.get(uid=instructor_uid)
            instance.instructors.add(instructor_obj)
        instance.save()
        return Response(
            {"message": f"Course {'added' if created else 'updated'} successfully."}
        )
    elif request.method == 'DELETE':
        instance = user.course_set.get(
            course_number=request.data['course_number'])
        instance.delete()
        return Response({"message": "Course deleted successfully."})


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def departmentView(request):
    user = request.user
    if request.method == 'GET':
        instance = user.department_set.all()
        serializer = DepartmentSerializer(instance, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        instance, created = user.department_set.get_or_create(
            dept_name=data['dept_name'])
        instance.owner = user
        for course_number in data['course_numbers']:
            course_obj = user.course_set.get(course_number=course_number)
            instance.courses.add(course_obj)
        instance.save()
        return Response(
            {"message": f"Department {'added' if created else 'updated'} successfully."}
        )
    elif request.method == 'DELETE':
        instance = user.department_set.get(
            dept_name=request.data['dept_name'])
        instance.delete()
        return Response({"message": "Department deleted successfully."})


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def sectionView(request):
    user = request.user
    if request.method == 'GET':
        instance = user.section_set.all()
        serializer = SectionSerializer(instance, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        department = user.department_set.get(
            dept_name=data['dept_name'])
        instance, created = user.section_set.get_or_create(
            section_id=data['section_id'], department=department)
        instance.owner = user
        instance.num_class_in_week = data['num_class_in_week']
        instance.course = user.course_set.get(
            course_number=data['course_number'])
        instance.meeting_time = user.meetingtime_set.get(pid=data['pid'])
        instance.room = user.room_set.get(r_number=data['r_number'])
        instance.instructor = user.instructor_set.get(uid=data['uid'])
        instance.save()
        return Response(
            {"message": f"Section {'added' if created else 'updated'} successfully."}
        )
    elif request.method == 'DELETE':
        instance = user.section_set.get(
            section_id=request.data['section_id'])
        instance.delete()
        return Response({"message": "Section deleted successfully."})
