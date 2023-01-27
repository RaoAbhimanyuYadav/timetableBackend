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

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.start_time = validated_data.get(
            'start_time', instance.start_time)
        instance.end_time = validated_data.get('end_time', instance.end_time)
        instance.save()
        return BellTimingSerializer(instance, many=False).data


class WorkingDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Working_Day
        fields = ['id', 'name', 'code']

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.code = validated_data.get('code', instance.code)
        instance.save()
        return WorkingDaySerializer(instance, many=False).data


class SubjectTimeOffSerializer(serializers.ModelSerializer):
    bell_timing = BellTimingSerializer(many=False)
    working_day = WorkingDaySerializer(many=False)

    class Meta:
        model = Subject_Time_Off
        fields = ['id', 'bell_timing', 'working_day']

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

        for data in validated_data['subject_time_off_set']:
            SubjectTimeOffSerializer().create(data, instance, user)

        return SubjectSerializer(instance, many=False).data

    def update(self, instance, validated_data, user):
        instance.name = validated_data.get('name', instance.name)
        instance.code = validated_data.get('code', instance.code)
        instance.save()

        new_data = validated_data.get('subject_time_off_set', [])
        old = instance.subject_time_off_set.all()
        old_data = SubjectTimeOffSerializer(old, many=True).data
        for data in old_data:
            if data not in new_data:
                # Remove already present data
                Subject_Time_Off.objects.get(id=data['id']).delete()
        # NEWLY ADDED
        for data in new_data:
            if 'id' not in data:
                SubjectTimeOffSerializer().create(data, instance, user)
        return SubjectSerializer(instance, many=False).data


class SemesterTimeOffSerializer(serializers.ModelSerializer):
    bell_timing = BellTimingSerializer(many=False)
    working_day = WorkingDaySerializer(many=False)

    class Meta:
        model = Semester_Time_Off
        fields = ['id', 'bell_timing', 'working_day']

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

        for data in validated_data['semester_time_off_set']:
            SemesterTimeOffSerializer().create(data, instance, user)

        for data in validated_data['semester_group_set']:
            SemesterGroupSerializer().create(data, instance, user)

        return SemesterSerializer(instance, many=False).data

    def update(self, instance, validated_data, user):
        instance.name = validated_data.get('name', instance.name)
        instance.code = validated_data.get('code', instance.code)
        instance.save()

        new_time_data = validated_data.get('semester_time_off_set', [])
        new_grp_data = validated_data.get('semester_group_set', [])
        old_time = instance.semester_time_off_set.all()
        old_time_data = SemesterTimeOffSerializer(old_time, many=True).data
        for data in old_time_data:
            if data not in new_time_data:
                # Remove already present data
                Semester_Time_Off.objects.get(id=data['id']).delete()
        # NEWLY ADDED
        for data in new_time_data:
            if 'id' not in data:
                SemesterTimeOffSerializer().create(data, instance, user)

        old_grp = instance.semester_group_set.all()
        old_grp_data = SemesterGroupSerializer(old_grp, many=True).data
        for data in old_grp_data:
            if data not in new_grp_data:
                # Remove already present data
                Semester_Group.objects.get(id=data['id']).delete()
        # NEWLY ADDED
        for data in new_grp_data:
            if 'id' not in data:
                SemesterGroupSerializer().create(data, instance, user)

        return SemesterSerializer(instance, many=False).data


class ClassroomTimeOffSerializer(serializers.ModelSerializer):
    bell_timing = BellTimingSerializer(many=False)
    working_day = WorkingDaySerializer(many=False)

    class Meta:
        model = Classroom_Time_Off
        fields = ['id', 'bell_timing', 'working_day']

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

        for data in validated_data['classroom_time_off_set']:
            ClassroomTimeOffSerializer().create(data, instance, user)

        return ClassroomSerializer(instance, many=False).data

    def update(self, instance, validated_data, user):
        instance.name = validated_data.get('name', instance.name)
        instance.code = validated_data.get('code', instance.code)
        instance.save()

        new_data = validated_data.get('classroom_time_off_set', [])
        old = instance.classroom_time_off_set.all()
        old_data = ClassroomTimeOffSerializer(old, many=True).data
        for data in old_data:
            if data not in new_data:
                # Remove already present data
                Classroom_Time_Off.objects.get(id=data['id']).delete()
        # NEWLY ADDED
        for data in new_data:
            if 'id' not in data:
                ClassroomTimeOffSerializer().create(data, instance, user)

        return ClassroomSerializer(instance, many=False).data


class TeacherTimeOffSerializer(serializers.ModelSerializer):
    bell_timing = BellTimingSerializer(many=False)
    working_day = WorkingDaySerializer(many=False)

    class Meta:
        model = Teacher_Time_Off
        fields = ["id", 'bell_timing', 'working_day']

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

        for data in validated_data['teacher_time_off_set']:
            TeacherTimeOffSerializer().create(data, instance, user)

        return TeacherSerializer(instance, many=False).data

    def update(self, instance, validated_data, user):
        instance.name = validated_data.get('name', instance.name)
        instance.code = validated_data.get('code', instance.code)
        instance.color = validated_data.get('color', instance.color)
        instance.save()

        new_data = validated_data.get('teacher_time_off_set', [])
        old = instance.teacher_time_off_set.all()
        old_data = TeacherTimeOffSerializer(old, many=True).data
        for data in old_data:
            if data not in new_data:
                # Remove already present data
                Teacher_Time_Off.objects.get(id=data['id']).delete()
        # NEWLY ADDED
        for data in new_data:
            if 'id' not in data:
                TeacherTimeOffSerializer().create(data, instance, user)

        return TeacherSerializer(instance, many=False).data


class LessonSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer(many=False)
    classroom = ClassroomSerializer(many=False)
    subject = SubjectSerializer(many=False)
    semester = SemesterSerializer(many=False)
    semester_group = SemesterGroupSerializer(many=False)

    class Meta:
        model = Lesson
        fields = [
            'id', 'teacher', 'classroom', 'subject',
            'semester', 'semester_group', 'lesson_per_week', 'is_lab']

    def create(self, data, user):
        teacher_inst = Teacher.objects.get(id=data['teacher']['id'])
        classroom_inst = Classroom.objects.get(id=data['classroom']['id'])
        subject_inst = Subject.objects.get(id=data['subject']['id'])
        semester_inst = Semester.objects.get(id=data['semester']['id'])
        semester_grp_inst = Semester_Group.objects.get(
            id=data['semester_group']['id'])
        lesson_per_week = data['lesson_per_week']
        is_lab = data['is_lab']
        instance = Lesson.objects.create(
            owner=user, teacher=teacher_inst, subject=subject_inst,
            classroom=classroom_inst, semester=semester_inst, semester_group=semester_grp_inst,
            lesson_per_week=lesson_per_week, is_lab=is_lab)
        return LessonSerializer(instance, many=False).data

    def update(self, instance, data, user):
        instance.lesson_per_week = data.get(
            'lesson_per_week', instance.lesson_per_week)
        instance.is_lab = data.get('is_lab', instance.is_lab)
        instance.teacher = Teacher.objects.get(id=data.get(
            'teacher', {}).get('id', instance.teacher.id))
        instance.classroom = Classroom.objects.get(
            id=data.get('classroom', {}).get('id', instance.classroom.id))
        instance.subject = Subject.objects.get(id=data.get(
            'subject', {}).get('id', instance.subject.id))
        instance.semester = Semester.objects.get(
            id=data.get('semester', {}).get('id', instance.semester.id))
        instance.semester_group = Semester_Group.objects.get(
            id=data.get('semester_group', {}).get('id', instance.semester_group.id))
        instance.save()
        return LessonSerializer(instance, many=False).data
