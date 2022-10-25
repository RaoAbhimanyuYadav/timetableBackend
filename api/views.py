from rest_framework.response import Response
from rest_framework.decorators import api_view

from timetable.models import Room, Instructor, MeetingTime, Course, Department, Section
from .serializers import (
    RoomSerializer, InstructorSerializer, MeetingTimeSerializer, CourseSerializer,
    DepartmentSerializer, SectionSerializer
)


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
        return Response(
            {"message": f"Instructor {'added' if created else 'updated'} successfully."}
        )
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


@api_view(['GET', 'POST', 'DELETE'])
def courseView(request):
    if request.method == 'GET':
        instance = Course.objects.all()
        serializer = CourseSerializer(instance, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        instance, created = Course.objects.get_or_create(
            course_number=data['course_number'])
        instance.course_name = data['course_name']
        instance.max_numb_students = data['max_numb_students']
        for instructor_uid in data['instructor_uids']:
            instructor_obj = Instructor.objects.get(uid=instructor_uid)
            instance.instructors.add(instructor_obj)
        instance.save()
        return Response(
            {"message": f"Course {'added' if created else 'updated'} successfully."}
        )
    elif request.method == 'DELETE':
        instance = Course.objects.get(
            course_number=request.data['course_number'])
        instance.delete()
        return Response({"message": "Course deleted successfully."})


@api_view(['GET', 'POST', 'DELETE'])
def departmentView(request):
    if request.method == 'GET':
        instance = Department.objects.all()
        serializer = DepartmentSerializer(instance, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        instance, created = Department.objects.get_or_create(
            dept_name=data['dept_name'])
        for course_number in data['course_numbers']:
            course_obj = Course.objects.get(course_number=course_number)
            instance.courses.add(course_obj)
        instance.save()
        return Response(
            {"message": f"Department {'added' if created else 'updated'} successfully."}
        )
    elif request.method == 'DELETE':
        instance = Department.objects.get(
            dept_name=request.data['dept_name'])
        instance.delete()
        return Response({"message": "Department deleted successfully."})


@api_view(['GET', 'POST', 'DELETE'])
def sectionView(request):
    if request.method == 'GET':
        instance = Section.objects.all()
        serializer = SectionSerializer(instance, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        department = Department.objects.get(
            dept_name=data['dept_name'])
        instance, created = Section.objects.get_or_create(
            section_id=data['section_id'], department=department)
        instance.num_class_in_week = data['num_class_in_week']
        instance.course = Course.objects.get(
            course_number=data['course_number'])
        instance.meeting_time = MeetingTime.objects.get(pid=data['pid'])
        instance.room = Room.objects.get(r_number=data['r_number'])
        instance.instructor = Instructor.objects.get(uid=data['uid'])
        instance.save()
        return Response(
            {"message": f"Section {'added' if created else 'updated'} successfully."}
        )
    elif request.method == 'DELETE':
        instance = Section.objects.get(
            section_id=request.data['section_id'])
        instance.delete()
        return Response({"message": "Section deleted successfully."})
