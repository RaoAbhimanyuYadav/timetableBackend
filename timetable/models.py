from django.db import models
from django.contrib.auth.models import User

import uuid


class Bell_Timing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)

    class Meta:
        unique_together = ('owner', 'start_time', 'end_time')

    def __str__(self):
        return f"On {self.name} {self.start_time} - {self.end_time}"


class Working_Day(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)

    class Meta:
        unique_together = ('owner', 'name',)

    def __str__(self):
        return f"On {self.name}"


class Subject(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)

    class Meta:
        unique_together = ('owner', 'code',)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Subject_Time_Off(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    bell_timing = models.ForeignKey(Bell_Timing, on_delete=models.CASCADE)
    working_day = models.ForeignKey(Working_Day, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)

    class Meta:
        unique_together = (
            'owner', 'subject_id', 'bell_timing', 'working_day')

    def __str__(self):
        return f"{self.subject_id}"


class Classroom(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)

    class Meta:
        unique_together = ('owner', 'code',)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Classroom_Time_Off(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    classroom_id = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    bell_timing = models.ForeignKey(Bell_Timing, on_delete=models.CASCADE)
    working_day = models.ForeignKey(Working_Day, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)

    class Meta:
        unique_together = (
            'owner', 'classroom_id', 'bell_timing', 'working_day')

    def __str__(self):
        return f"{self.classroom_id}"


class Semester(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=25)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)

    class Meta:
        unique_together = ('owner', 'code',)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Semester_Group(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    semester_id = models.ForeignKey(Semester, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)

    class Meta:
        unique_together = ('owner', 'code', 'semester_id')

    def __str__(self):
        return f"{self.name} ({self.code})"


class Semester_Time_Off(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    semester_id = models.ForeignKey(Semester, on_delete=models.CASCADE)
    bell_timing = models.ForeignKey(Bell_Timing, on_delete=models.CASCADE)
    working_day = models.ForeignKey(Working_Day, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)

    class Meta:
        unique_together = (
            'owner', 'semester_id', 'bell_timing', 'working_day')

    def __str__(self):
        return f"{self.semester_id}"


class Teacher(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=25)
    color = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)

    class Meta:
        unique_together = ('owner', 'code',)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Teacher_Time_Off(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    bell_timing = models.ForeignKey(Bell_Timing, on_delete=models.CASCADE)
    working_day = models.ForeignKey(Working_Day, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)

    class Meta:
        unique_together = (
            'owner', 'teacher_id', 'bell_timing', 'working_day')

    def __str__(self):
        return f"{self.teacher_id}"


class Lesson(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    teacher = models.ManyToManyField(Teacher)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    semester = models.ManyToManyField(Semester)
    semester_group = models.ManyToManyField(Semester_Group)
    lesson_per_week = models.IntegerField(default=1)
    is_lab = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)

    def __str__(self):
        return f"{self.classroom} {self.subject}"
