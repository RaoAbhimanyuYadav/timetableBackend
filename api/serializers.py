from rest_framework import serializers

from timetable.models import (
    Bell_Timing, Working_Day, Lesson,
    Subject, Time_Off,
    Semester, Semester_Group,
    Classroom,     Teacher, )

from .functions import set_time_off_handler, set_handler_with_time_off


class BellTimingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bell_Timing
        exclude = ['owner', 'created_at']


class WorkingDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Working_Day
        fields = ['id', 'c_id', 'name', 'code']


class TimeOffSerializer(serializers.ModelSerializer):
    bell_timing = BellTimingSerializer(many=False)
    working_day = WorkingDaySerializer(many=False)

    class Meta:
        model = Time_Off
        exclude = ['owner']


class SubjectSerializer(serializers.ModelSerializer):
    time_off = TimeOffSerializer(many=True, read_only=True)

    class Meta:
        model = Subject
        exclude = ["owner", "created_at"]
        extra_kwargs = {'time_off': {'required': False}}

    def create(self, validated_data):
        instance = Subject.objects.create(
            code=validated_data['code'],
            owner=validated_data['owner'],
            name=validated_data['name']
        )

        for data in validated_data['time_off']:
            t_inst = Time_Off.objects.get(
                bell_timing=data['bell_timing']['id'],
                working_day=data['working_day']['id']
            )
            instance.time_off.add(t_inst)

        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.code = validated_data.get('code', instance.code)
        instance.time_off.clear()

        for data in validated_data['time_off']:
            t_inst = Time_Off.objects.get(
                bell_timing=data['bell_timing']['id'],
                working_day=data['working_day']['id']
            )
            instance.time_off.add(t_inst)

        instance.save()
        return instance


class ClassroomSerializer(serializers.ModelSerializer):
    time_off = TimeOffSerializer(many=True, read_only=True)

    class Meta:
        model = Classroom
        exclude = ['owner', 'created_at']
        extra_kwargs = {'time_off': {'required': False}}

    def create(self, validated_data):
        instance = Classroom.objects.create(
            code=validated_data['code'],
            name=validated_data['name'],
            owner=validated_data['owner']
        )

        for data in validated_data['time_off']:
            t_inst = Time_Off.objects.get(
                bell_timing=data['bell_timing']['id'],
                working_day=data['working_day']['id']
            )
            instance.time_off.add(t_inst)

        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.code = validated_data.get('code', instance.code)

        instance.time_off.clear()

        for data in validated_data['time_off']:
            t_inst = Time_Off.objects.get(
                bell_timing=data['bell_timing']['id'],
                working_day=data['working_day']['id']
            )
            instance.time_off.add(t_inst)

        instance.save()
        return instance


# class SemesterTimeOffSerializer(serializers.ModelSerializer):
#     bell_timing = BellTimingSerializer(many=False)
#     working_day = WorkingDaySerializer(many=False)

#     class Meta:
#         model = Semester_Time_Off
#         fields = ['id', 'bell_timing', 'working_day']

#     def create(self, validated_data, instance, user):
#         return set_time_off_handler(
#             validated_data, instance, user, 'semester', Semester_Time_Off)


# class SemesterGroupSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Semester_Group
#         fields = ['id', 'name', 'code']

#     def create(self, data, instance, user):
#         return Semester_Group.objects.create(
#             owner=user, name=data['name'], code=data['code'], semester=instance)


# class SemesterSerializer(serializers.ModelSerializer):
#     semester_time_off_set = SemesterTimeOffSerializer(many=True)
#     semester_group_set = SemesterGroupSerializer(many=True)
#     classroom = ClassroomSerializer(many=False)

#     class Meta:
#         model = Semester
#         fields = [
#             'id', 'name', 'code', 'classroom', 'semester_time_off_set', 'semester_group_set']

#     def create(self, validated_data, user):
#         classroom = Classroom.objects.get(
#             id=validated_data['classroom']['id'])
#         kwargs = {}
#         for key in ['name', 'code']:
#             kwargs[key] = validated_data[key]
#         instance = Semester.objects.create(
#             owner=user, **kwargs, classroom=classroom)

#         for data in validated_data['semester_time_off_set']:
#             SemesterTimeOffSerializer().create(data, instance, user)

#         for data in validated_data['semester_group_set']:
#             SemesterGroupSerializer().create(data, instance, user)

#         return SemesterSerializer(instance, many=False).data

#     def update(self, instance, validated_data, user):
#         instance.name = validated_data.get('name', instance.name)
#         instance.code = validated_data.get('code', instance.code)
#         instance.classroom = Classroom.objects.get(
#             id=validated_data.get('classroom', {}).get('id', instance.classroom.id))
#         instance.save()

#         new_time_data = validated_data.get('semester_time_off_set', [])
#         new_grp_data = validated_data.get('semester_group_set', [])
#         old_time = instance.semester_time_off_set.all()
#         old_time_data = SemesterTimeOffSerializer(old_time, many=True).data
#         for data in old_time_data:
#             if data not in new_time_data:
#                 # Remove already present data
#                 Semester_Time_Off.objects.get(id=data['id']).delete()
#         # NEWLY ADDED
#         for data in new_time_data:
#             if 'id' not in data:
#                 SemesterTimeOffSerializer().create(data, instance, user)

#         old_grp = instance.semester_group_set.all()
#         old_grp_data = SemesterGroupSerializer(old_grp, many=True).data
#         for data in old_grp_data:
#             if data not in new_grp_data:
#                 # Remove already present data
#                 Semester_Group.objects.get(id=data['id']).delete()
#         # NEWLY ADDED
#         for data in new_grp_data:
#             if 'id' not in data:
#                 SemesterGroupSerializer().create(data, instance, user)

#         return SemesterSerializer(instance, many=False).data


# class TeacherTimeOffSerializer(serializers.ModelSerializer):
#     bell_timing = BellTimingSerializer(many=False)
#     working_day = WorkingDaySerializer(many=False)

#     class Meta:
#         model = Teacher_Time_Off
#         fields = ["id", 'bell_timing', 'working_day']

#     def create(self, validated_data, instance, user):
#         return set_time_off_handler(
#             validated_data, instance, user, 'teacher_id', Teacher_Time_Off)


# class TeacherSerializer(serializers.ModelSerializer):
#     teacher_time_off_set = TeacherTimeOffSerializer(many=True)

#     class Meta:
#         model = Teacher
#         fields = ['id', 'name', 'code', 'color',
#                   'teacher_time_off_set', 'lesson_set']

#     def create(self, validated_data, user):
#         instance = set_handler_with_time_off(
#             Teacher, user, validated_data, ['name', 'code', 'color'])

#         for data in validated_data['teacher_time_off_set']:
#             TeacherTimeOffSerializer().create(data, instance, user)

#         return TeacherSerializer(instance, many=False).data

#     def update(self, instance, validated_data, user):
#         instance.name = validated_data.get('name', instance.name)
#         instance.code = validated_data.get('code', instance.code)
#         instance.color = validated_data.get('color', instance.color)
#         instance.save()

#         new_data = validated_data.get('teacher_time_off_set', [])
#         old = instance.teacher_time_off_set.all()
#         old_data = TeacherTimeOffSerializer(old, many=True).data
#         for data in old_data:
#             if data not in new_data:
#                 # Remove already present data
#                 Teacher_Time_Off.objects.get(id=data['id']).delete()
#         # NEWLY ADDED
#         for data in new_data:
#             if 'id' not in data:
#                 TeacherTimeOffSerializer().create(data, instance, user)

#         return TeacherSerializer(instance, many=False).data


# class LessonSerializer(serializers.ModelSerializer):
#     classroom = ClassroomSerializer(many=False)
#     subject = SubjectSerializer(many=False)
#     semester = SemesterSerializer(many=True)
#     semester_group = SemesterGroupSerializer(many=True)
#     teacher = TeacherSerializer(many=True)

#     class Meta:
#         model = Lesson
#         fields = [
#             'id',  'teacher', 'classroom', 'subject',
#             'semester', 'semester_group', 'lesson_per_week', 'lesson_length']

#     def create(self, data, user):
#         classroom_inst = Classroom.objects.get(id=data['classroom']['id'])
#         subject_inst = Subject.objects.get(id=data['subject']['id'])
#         lesson_per_week = data['lesson_per_week']
#         lesson_length = data['lesson_length']

#         instance = Lesson.objects.create(
#             owner=user, subject=subject_inst, classroom=classroom_inst,
#             lesson_per_week=lesson_per_week, lesson_length=lesson_length)

#         for t_id in data['teacher']:
#             teacher_inst = Teacher.objects.get(id=t_id['id'])
#             instance.teacher.add(teacher_inst)

#         for s_id in data['semester']:
#             semester_inst = Semester.objects.get(id=s_id['id'])
#             instance.semester.add(semester_inst)

#         for g_id in data['semester_group']:
#             semester_grp_inst = Semester_Group.objects.get(id=g_id['id'])
#             instance.semester_group.add(semester_grp_inst)

#         return LessonSerializer(instance, many=False).data

#     def update(self, instance, data, user):
#         instance.lesson_per_week = data.get(
#             'lesson_per_week', instance.lesson_per_week)
#         instance.lesson_length = data.get(
#             'lesson_length', instance.lesson_length)
#         instance.subject = Subject.objects.get(id=data.get(
#             'subject', {}).get('id', instance.subject.id))
#         instance.classroom = Classroom.objects.get(
#             id=data.get('classroom', {}).get('id', instance.classroom.id))

#         new_set = []
#         for t_id in data['teacher']:
#             teacher_inst = Teacher.objects.get(id=t_id['id'])
#             new_set.append(teacher_inst)
#         instance.teacher.set(new_set)

#         new_set = []
#         for s_id in data['semester']:
#             semester_inst = Semester.objects.get(id=s_id['id'])
#             new_set.append(semester_inst)
#         instance.semester.set(new_set)

#         new_set = []
#         for g_id in data['semester_group']:
#             semester_grp_inst = Semester_Group.objects.get(id=g_id['id'])
#             new_set.append(semester_grp_inst)
#         instance.semester_group.set(new_set)

#         instance.save()
#         return LessonSerializer(instance, many=False).data


# class TeacherFormatSerializer(serializers.ModelSerializer):
#     teacher_time_off_set = TeacherTimeOffSerializer(many=True)

#     class Meta:
#         model = Teacher
#         fields = ['id', "name", "code", "color", "teacher_time_off_set"]


# class SemesterFormatSerializer(serializers.ModelSerializer):
#     total_groups = serializers.SerializerMethodField('get_total_groups')
#     semester_time_off_set = SemesterTimeOffSerializer(many=True)
#     w_id = serializers.SerializerMethodField('get_w_id')

#     def get_w_id(self, sem):
#         return sem.semester_group_set.filter(code="W")[0].id

#     def get_total_groups(self, sem):
#         return sem.semester_group_set.all().__len__() - 1

#     class Meta:
#         model = Semester
#         fields = ["id", "name", "code",
#                   "semester_time_off_set", "total_groups", "w_id"]


# class SemesterGroupFormatSerializer(serializers.ModelSerializer):
#     semester = SemesterFormatSerializer(many=False)

#     class Meta:
#         model = Semester_Group
#         fields = ['id', 'name', 'code', "semester"]


# class LessonFormatSerializer(serializers.ModelSerializer):
#     classroom = ClassroomSerializer(many=False)
#     subject = SubjectSerializer(many=False)
#     semester_group = SemesterGroupFormatSerializer(many=True)
#     teacher = TeacherFormatSerializer(many=True)

#     class Meta:
#         model = Lesson
#         fields = ["id",  "teacher", "classroom", "subject",
#                   "semester_group", "lesson_per_week", "lesson_length"]
