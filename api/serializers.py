from rest_framework import serializers
from django.core.exceptions import ValidationError

from timetable.models import (
    Bell_Timing, Working_Day, Lesson,
    Subject, Time_Off,
    Semester, Semester_Group,
    Classroom, Teacher)

from .functions import add_time_off_handler


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

        add_time_off_handler(instance, validated_data)
        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.code = validated_data.get('code', instance.code)
        instance.save()

        add_time_off_handler(instance, validated_data)
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

        add_time_off_handler(instance, validated_data)
        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.code = validated_data.get('code', instance.code)
        instance.save()

        add_time_off_handler(instance, validated_data)

        return instance


class SemesterGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Semester_Group
        exclude = ['owner', 'created_at']


class SemesterSerializer(serializers.ModelSerializer):
    time_off = TimeOffSerializer(many=True, read_only=True)
    groups = SemesterGroupSerializer(many=True, read_only=True)
    classroom = ClassroomSerializer(many=False, read_only=True)

    class Meta:
        model = Semester
        exclude = ['owner', 'created_at']

    def create(self, validated_data):
        try:
            c_inst = Classroom.objects.get(
                id=validated_data.get('classroom', {}).get('id', ''))

            instance = Semester.objects.create(
                code=validated_data['code'],
                name=validated_data['name'],
                owner=validated_data['owner'],
                classroom=c_inst)

            add_time_off_handler(instance, validated_data)

            for data in validated_data['groups']:
                g_inst = Semester_Group.objects.get(
                    id=data['id']
                )
                instance.groups.add(g_inst)

            instance.save()
            return instance
        except Classroom.DoesNotExist:
            raise Exception(
                "Please enter correct classroom")
        except Semester_Group.DoesNotExist:
            instance.delete()
            raise Exception(
                "Please enter correct Semester Group")
        except ValidationError:
            raise Exception(
                "Please enter correct id of classroom or semester group")

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.code = validated_data.get('code', instance.code)
        instance.save()
        try:
            instance.classroom = Classroom.objects.get(
                id=validated_data.get('classroom', {}).get('id', instance.classroom.id))
            instance.save()

            add_time_off_handler(instance, validated_data)

            instance.groups.clear()
            for data in validated_data['groups']:
                g_inst = Semester_Group.objects.get(
                    id=data['id']
                )
                instance.groups.add(g_inst)

            instance.save()
            return instance
        except Semester.DoesNotExist:
            raise Semester.DoesNotExist(
                "Please enter correct semester", instance)
        except Semester_Group.DoesNotExist:
            raise Exception(
                "Please enter correct Semester Group")
        except ValidationError:
            raise Semester.DoesNotExist(
                "Please enter correct semester", instance)


class TeacherSerializer(serializers.ModelSerializer):
    time_off = TimeOffSerializer(many=True, read_only=True)

    class Meta:
        model = Teacher
        exclude = ['owner', 'created_at']

    def create(self, validated_data):
        instance = Teacher(
            code=validated_data['code'],
            owner=validated_data['owner'],
            name=validated_data['name'],
            color=validated_data['color']
        )
        instance.save()

        add_time_off_handler(instance, validated_data)
        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.code = validated_data.get('code', instance.code)
        instance.color = validated_data.get('color', instance.color)
        instance.save()

        add_time_off_handler(instance, validated_data)
        return instance


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
