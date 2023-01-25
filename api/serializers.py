from rest_framework import serializers

from timetable.models import (
    Bell_Timing, Working_Day, Lesson,
    Subject, Subject_Time_Off,
    Semester, Semester_Group, Semester_Time_Off,
    Classroom, Classroom_Time_Off,
    Teacher, Teacher_Time_Off, )

from .functions import set_time_off_handler, set_handler


class BellTimingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bell_Timing
        fields = ['id', 'name', 'start_time', 'end_time']


class WorkingDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Working_Day
        fields = ['id', 'name', 'code']


class SubjectTimeOffSerializer(serializers.ModelSerializer):
    bell_timing = BellTimingSerializer(many=False)
    working_day = WorkingDaySerializer(many=False)

    class Meta:
        model = Subject_Time_Off
        fields = ['bell_timing', 'working_day']

    def create(self, validated_data, subject_id, user):
        return set_time_off_handler(
            validated_data, subject_id, user, 'subject_id', Subject, Subject_Time_Off)


class SubjectSerializer(serializers.ModelSerializer):
    subject_time_off_set = SubjectTimeOffSerializer(many=True)

    class Meta:
        model = Subject
        fields = ['id', 'name', 'code', 'subject_time_off_set']

    def create(self, validated_data, user):
        instance = set_handler(Subject, user, validated_data, ['name', 'code'])
        for data in validated_data['subject_time_off_set']:
            SubjectTimeOffSerializer().create(data, instance.id, user)
        return instance


class SemesterTimeOffSerializer(serializers.ModelSerializer):
    bell_timing = BellTimingSerializer(many=False)
    working_day = WorkingDaySerializer(many=False)

    class Meta:
        model = Semester_Time_Off
        fields = ['bell_timing', 'working_day']

    def create(self, validated_data, id, user):
        return set_time_off_handler(
            validated_data, id, user, 'semester_id', Semester, Semester_Time_Off)


class SemesterGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Semester_Group
        fields = ['id', 'name', 'code']

    def create(self, data, id, user):
        instance = Semester.objects.get(id=id)
        return Semester_Group.objects.create(
            owner=user, name=data['name'], code=data['code'], semester_id=instance)


class SemesterSerializer(serializers.ModelSerializer):
    semester_time_off_set = SemesterTimeOffSerializer(many=True)
    semester_group_set = SemesterGroupSerializer(many=True)

    class Meta:
        model = Semester
        fields = [
            'id', 'name', 'code', 'semester_time_off_set', 'semester_group_set']

    def create(self, validated_data, user):
        instance = set_handler(
            Semester, user, validated_data, ['name', 'code'])
        for data in validated_data['semester_time_off_set']:
            SemesterTimeOffSerializer().create(data, instance.id, user)
        for data in validated_data['semester_group_set']:
            SemesterGroupSerializer().create(data, instance.id, user)
        return instance


class ClassroomTimeOffSerializer(serializers.ModelSerializer):
    bell_timing = BellTimingSerializer(many=False)
    working_day = WorkingDaySerializer(many=False)

    class Meta:
        model = Classroom_Time_Off
        fields = ['bell_timing', 'working_day']

    def create(self, validated_data, id, user):
        return set_time_off_handler(
            validated_data, id, user, 'classroom_id', Classroom, Classroom_Time_Off)


class ClassroomSerializer(serializers.ModelSerializer):
    classroom_time_off_set = ClassroomTimeOffSerializer(many=True)

    class Meta:
        model = Classroom
        fields = ['id', 'name', 'code', 'classroom_time_off_set']

    def create(self, validated_data, user):
        instance = set_handler(
            Classroom, user, validated_data, ['name', 'code'])
        for data in validated_data['classroom_time_off_set']:
            ClassroomTimeOffSerializer().create(data, instance.id, user)
        return instance


class TeacherTimeOffSerializer(serializers.ModelSerializer):
    bell_timing = BellTimingSerializer(many=False)
    working_day = WorkingDaySerializer(many=False)

    class Meta:
        model = Teacher_Time_Off
        fields = ['bell_timing', 'working_day']

    def create(self, validated_data, id, user):
        return set_time_off_handler(
            validated_data, id, user, 'teacher_id', Teacher, Teacher_Time_Off)


class TeacherSerializer(serializers.ModelSerializer):
    teacher_time_off_set = TeacherTimeOffSerializer(many=True)

    class Meta:
        model = Teacher
        fields = ['id', 'name', 'code', 'color', 'teacher_time_off_set']

    def create(self, validated_data, user):
        instance = set_handler(
            Teacher, user, validated_data, ['name', 'code', 'color'])
        for data in validated_data['teacher_time_off_set']:
            TeacherTimeOffSerializer().create(data, instance.id, user)
        return instance


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
