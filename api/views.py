from rest_framework.response import Response
from rest_framework.decorators import api_view

from timetable.models import Room, Instructor, MeetingTime, Course, Department, Section
from .serializers import RoomSerializer


@api_view(['GET'])
def getRoutes(request):

    routes = [
        {"GET", "/api/v1/"},
        {"GET", "/api/v1/rooms"},
    ]

    return Response(routes)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def room(request):
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
