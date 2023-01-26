from rest_framework import serializers

from timetable.models import (
    Bell_Timing, Working_Day, Lesson,
    Subject, Subject_Time_Off,
    Semester, Semester_Group, Semester_Time_Off,
    Classroom, Classroom_Time_Off,
    Teacher, Teacher_Time_Off, )

from .functions import set_time_off_handler, set_handler_with_time_off


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

    def create(self, validated_data, instance, user):
        return set_time_off_handler(
            validated_data, instance, user, 'subject_id', Subject_Time_Off)


class SubjectSerializer(serializers.ModelSerializer):
    subject_time_off_set = SubjectTimeOffSerializer(many=True)

    class Meta:
        model = Subject
        fields = ['id', 'name', 'code', 'subject_time_off_set']

    def create(self, validated_data, user):
        instance = set_handler_with_time_off(
            Subject, user, validated_data, ['name', 'code'])
        serialized = SubjectSerializer(instance, many=False).data
        serialized['subject_time_off_set'] = []
        for data in validated_data['subject_time_off_set']:
            time_off_instance = SubjectTimeOffSerializer().create(data, instance, user)
            serialized['subject_time_off_set'].append(
                SubjectTimeOffSerializer(time_off_instance, many=False).data)
        return serialized


class SemesterTimeOffSerializer(serializers.ModelSerializer):
    bell_timing = BellTimingSerializer(many=False)
    working_day = WorkingDaySerializer(many=False)

    class Meta:
        model = Semester_Time_Off
        fields = ['bell_timing', 'working_day']

    def create(self, validated_data, instance, user):
        return set_time_off_handler(
            validated_data, instance, user, 'semester_id', Semester_Time_Off)


class SemesterGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Semester_Group
        fields = ['id', 'name', 'code']

    def create(self, data, instance, user):
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
        instance = set_handler_with_time_off(
            Semester, user, validated_data, ['name', 'code'])
        serialized = SemesterSerializer(instance, many=False).data
        serialized['semester_time_off_set'] = []
        for data in validated_data['semester_time_off_set']:
            time_off_instance = SemesterTimeOffSerializer().create(data, instance, user)
            serialized['semester_time_off_set'].append(
                SemesterTimeOffSerializer(time_off_instance, many=False).data
            )
        serialized['semester_group_set'] = []
        for data in validated_data['semester_group_set']:
            sem_grp_instance = SemesterGroupSerializer().create(data, instance, user)
            serialized['semester_group_set'].append(
                SemesterGroupSerializer(sem_grp_instance, many=False).data
            )

        return serialized


class ClassroomTimeOffSerializer(serializers.ModelSerializer):
    bell_timing = BellTimingSerializer(many=False)
    working_day = WorkingDaySerializer(many=False)

    class Meta:
        model = Classroom_Time_Off
        fields = ['bell_timing', 'working_day']

    def create(self, validated_data, instance, user):
        return set_time_off_handler(
            validated_data, instance, user, 'classroom_id',  Classroom_Time_Off)


class ClassroomSerializer(serializers.ModelSerializer):
    classroom_time_off_set = ClassroomTimeOffSerializer(many=True)

    class Meta:
        model = Classroom
        fields = ['id', 'name', 'code', 'classroom_time_off_set']

    def create(self, validated_data, user):
        instance = set_handler_with_time_off(
            Classroom, user, validated_data, ['name', 'code'])
        serialized = ClassroomSerializer(instance, many=False).data
        serialized['classroom_time_off_set'] = []
        for data in validated_data['classroom_time_off_set']:
            time_off_instance = ClassroomTimeOffSerializer().create(data, instance, user)
            serialized['classroom_time_off_set'].append(
                ClassroomTimeOffSerializer(time_off_instance, many=False).data)
        return serialized


class TeacherTimeOffSerializer(serializers.ModelSerializer):
    bell_timing = BellTimingSerializer(many=False)
    working_day = WorkingDaySerializer(many=False)

    class Meta:
        model = Teacher_Time_Off
        fields = ['bell_timing', 'working_day']

    def create(self, validated_data, instance, user):
        return set_time_off_handler(
            validated_data, instance, user, 'teacher_id', Teacher_Time_Off)


class TeacherSerializer(serializers.ModelSerializer):
    teacher_time_off_set = TeacherTimeOffSerializer(many=True)

    class Meta:
        model = Teacher
        fields = ['id', 'name', 'code', 'color', 'teacher_time_off_set']

    def create(self, validated_data, user):
        instance = set_handler_with_time_off(
            Teacher, user, validated_data, ['name', 'code', 'color'])
        serialized = TeacherSerializer(instance, many=False).data
        serialized['teacher_time_off_set'] = []
        for data in validated_data['teacher_time_off_set']:
            time_off_instance = TeacherTimeOffSerializer().create(data, instance, user)
            serialized['teacher_time_off_set'].append(
                TeacherTimeOffSerializer(time_off_instance, many=False).data)
        return serialized


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
