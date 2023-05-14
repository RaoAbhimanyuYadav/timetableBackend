from rest_framework import serializers
from django.core.exceptions import ValidationError

from timetable.models import (
    Bell_Timing, Working_Day, Lesson,
    Subject, Time_Off,
    Semester, Group,
    Classroom, Teacher, SemGrpCombo,
    Saved_Timetable
)

from .functions import add_time_off_handler
import uuid


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


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        exclude = ['owner', 'created_at']


class SemesterSerializer(serializers.ModelSerializer):
    time_off = TimeOffSerializer(many=True, read_only=True)
    groups = GroupSerializer(many=True, read_only=True)
    classroom = ClassroomSerializer(many=False, read_only=True)
    w_id = serializers.SerializerMethodField('get_w_id')

    def get_w_id(self, sem):
        if sem.groups.filter(code="W").__len__() > 0:
            return sem.groups.filter(code="W")[0].id
        return ""

    class Meta:
        model = Semester
        exclude = ['owner', 'created_at']

    def create(self, validated_data):
        try:
            instance = Semester(
                code=validated_data['code'],
                name=validated_data['name'],
                owner=validated_data['owner'])
            c_inst = Classroom.objects.get(
                id=validated_data.get('classroom', {}).get('id', ''))

            instance.classroom = c_inst
            instance.save()

            add_time_off_handler(instance, validated_data)

            groups_inst = []
            for data in validated_data['groups']:
                g_inst = Group.objects.get(
                    id=data['id']
                )
                groups_inst.append(g_inst)
            for grp_inst in groups_inst:
                instance.groups.add(grp_inst)
            instance.save()
            return instance
        except Classroom.DoesNotExist:
            raise Exception(
                "Please enter correct classroom")
        except Group.DoesNotExist:
            instance.delete()
            raise Exception(
                "Please enter correct Semester Group")
        except ValidationError:
            instance.delete()
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

            groups_inst = []
            for data in validated_data['groups']:
                g_inst = Group.objects.get(
                    id=data['id']
                )
                groups_inst.append(g_inst)

            instance.groups.clear()
            for grp_inst in groups_inst:
                instance.groups.add(grp_inst)
            instance.save()
            return instance
        except Semester.DoesNotExist:
            raise Semester.DoesNotExist(
                "Please enter correct semester", instance)
        except Group.DoesNotExist:
            raise Exception(
                "Please enter correct Semester Group")
        except ValidationError:
            raise Semester.DoesNotExist(
                "Please enter correct semester", instance)
        except Exception:
            raise Exception("Please provide Group ID")


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


class SemGrpComboSerializer(serializers.ModelSerializer):
    semester = SemesterSerializer(many=False)
    group = GroupSerializer(many=False)

    class Meta:
        model = SemGrpCombo
        fields = ['semester', 'group']


class LessonSerializer(serializers.ModelSerializer):
    classroom = ClassroomSerializer(many=False, read_only=True)
    subject = SubjectSerializer(many=False, read_only=True)
    teachers = TeacherSerializer(many=True, read_only=True)
    sem_grps = serializers.SerializerMethodField('get_sem_grps')

    def get_sem_grps(self, instance):
        sem_grp_inst = SemGrpCombo.objects.filter(lesson=instance)
        data = []
        for inst in sem_grp_inst:
            data.append(SemGrpComboSerializer(instance=inst).data)
        return data

    class Meta:
        model = Lesson
        fields = [
            'id', 'teachers', 'classroom', 'subject',
            'lesson_per_week', 'lesson_length', 'sem_grps'
        ]

    def create(self, validated_data):
        try:
            instance = Lesson(
                owner=validated_data['owner'],
                lesson_per_week=validated_data.get('lesson_per_week', 1),
                lesson_length=validated_data.get('lesson_length', 1)
            )
            instance.classroom = Classroom.objects.get(
                id=validated_data
                    .get('classroom', {})
                    .get('id', uuid.uuid4())
            )
            instance.subject = Subject.objects.get(
                id=validated_data
                    .get('subject', {})
                    .get('id', uuid.uuid4())
            )
            instance.save()

            for t_id in validated_data['teachers']:
                teacher_inst = Teacher.objects.get(
                    id=t_id.get("id", uuid.uuid4()))
                instance.teachers.add(teacher_inst)

            for sem_grp in validated_data['sem_grps']:
                sem_inst = Semester.objects.get(
                    id=sem_grp
                    .get('semester', {})
                    .get('id', uuid.uuid4())
                )
                grp_inst = Group.objects.get(
                    id=sem_grp
                    .get('group', {})
                    .get('id', uuid.uuid4())
                )
                SemGrpCombo.objects.create(
                    lesson=instance,
                    semester=sem_inst,
                    group=grp_inst
                )

            return instance
        except Classroom.DoesNotExist:
            raise Exception("Enter a valid classroom.")
        except Subject.DoesNotExist:
            raise Exception("Enter a valid Subject.")
        except Teacher.DoesNotExist:
            instance.delete()
            raise Exception("Enter valid teachers.")
        except Semester.DoesNotExist:
            SemGrpCombo.objects.filter(lesson=instance).delete()
            instance.delete()
            raise Exception("Enter valid semesters.")
        except Group.DoesNotExist:
            SemGrpCombo.objects.filter(lesson=instance).delete()
            instance.delete()
            raise Exception("Enter valid groups.")
        except ValidationError as err:
            SemGrpCombo.objects.filter(lesson=instance).delete()
            instance.delete()
            raise Exception(err.args[0])

    def update(self, instance, validated_data):
        try:
            instance.lesson_per_week = validated_data.get(
                'lesson_per_week', instance.lesson_per_week)
            instance.lesson_length = validated_data.get(
                'lesson_length', instance.lesson_length)

            instance.subject = Subject.objects.get(id=validated_data.get(
                'subject', {}).get('id', instance.subject.id))
            instance.classroom = Classroom.objects.get(
                id=validated_data.get('classroom', {}).get('id', instance.classroom.id))
            instance.save()

            if validated_data.get('teachers', []).__len__() == 0:
                raise Time_Off.DoesNotExist(
                    "teachers can't be empty", instance)

            teachers_inst = []
            for t_id in validated_data.get('teachers', []):
                teacher_inst = Teacher.objects.get(
                    id=t_id.get("id", uuid.uuid4()))
                teachers_inst.append(teacher_inst)

            instance.teachers.clear()
            for t_inst in teachers_inst:
                instance.teachers.add(t_inst)
            instance.save()

            if validated_data.get('sem_grps', []).__len__() == 0:
                raise Time_Off.DoesNotExist(
                    "Sem_grps can't be empty", instance)
            sem_grps = []
            for sem_grp in validated_data['sem_grps']:
                sem_inst = Semester.objects.get(
                    id=sem_grp
                    .get('semester', {})
                    .get('id', uuid.uuid4())
                )
                grp_inst = Group.objects.get(
                    id=sem_grp
                    .get('group', {})
                    .get('id', uuid.uuid4())
                )
                sem_grps.append((sem_inst, grp_inst))

            SemGrpCombo.objects.filter(lesson=instance).delete()
            for sem_grp in sem_grps:
                SemGrpCombo.objects.create(
                    lesson=instance,
                    semester=sem_grp[0],
                    group=sem_grp[1]
                )
            instance.save()
            return instance
        except Classroom.DoesNotExist:
            raise Exception("Enter a valid classroom.")
        except Subject.DoesNotExist:
            raise Exception("Enter a valid Subject.")
        except Teacher.DoesNotExist:
            raise Time_Off.DoesNotExist("Enter valid teachers.", instance)
        except Semester.DoesNotExist:
            raise Time_Off.DoesNotExist("Enter valid semester.", instance)
        except Group.DoesNotExist:
            raise Time_Off.DoesNotExist("Enter valid groups.", instance)
        except ValidationError as err:
            raise Time_Off.DoesNotExist(
                err.args[0], instance)


class SavedTimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saved_Timetable
        exclude = ['owner']


class SavedWithoutDataTimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saved_Timetable
        exclude = ['owner', 'extra_lessons', 'data']
