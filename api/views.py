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


@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)
