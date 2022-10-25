from rest_framework.response import Response
from rest_framework.decorators import api_view

from timetable.models import Room, Instructor, MeetingTime, Course, Department, Section
from .serializers import RoomSerializer, InstructorSerializer, MeetingTimeSerializer, CourseSerializer, DepartmentSerializer, SectionSerializer


@api_view(['GET'])
def getRoutes(request):

    routes = [
        {"GET", "/api/v1/"},
        {"GET", "/api/v1/rooms"},
    ]

    return Response(routes)


@api_view(['GET', 'POST', 'DELETE'])
def roomView(request):
    if request.method == 'GET':
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        room, created = Room.objects.get_or_create(r_number=data['r_number'])
        room.seating_capacity = data['seating_capacity']
        room.save()
        return Response({"message": f"Room {'added' if created else 'updated'} successfully."})
    elif request.method == 'DELETE':
        room = Room.objects.get(r_number=request.data['r_number'])
        room.delete()
        return Response({"message": "Room deleted successfully."})


@api_view(['GET', 'POST', 'DELETE'])
def instructorView(request):
    if request.method == 'GET':
        instruc = Instructor.objects.all()
        serializer = InstructorSerializer(instruc, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        instruc, created = Instructor.objects.get_or_create(
            uid=data['uid'])
        instruc.name = data['name']
        instruc.save()
        return Response({"message": f"Instructor {'added' if created else 'updated'} successfully."})
    elif request.method == 'DELETE':
        instruc = Instructor.objects.get(uid=request.data['uid'])
        instruc.delete()
        return Response({"message": "Instructor deleted successfully."})


@api_view(['GET', 'POST', 'DELETE'])
def meetingTimeView(request):
    if request.method == 'GET':
        instance = MeetingTime.objects.all()
        serializer = MeetingTimeSerializer(instance, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        instance, created = MeetingTime.objects.get_or_create(
            pid=data['pid'])
        instance.time = data['time']
        instance.day = data['day']
        instance.save()
        return Response(
            {"message": f"Meeting Time {'added' if created else 'updated'} successfully."}
        )
    elif request.method == 'DELETE':
        instance = MeetingTime.objects.get(pid=request.data['pid'])
        instance.delete()
        return Response({"message": "Meeting Time deleted successfully."})
