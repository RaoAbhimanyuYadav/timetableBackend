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
    c_id = models.CharField(max_length=64, unique=True, default=uuid.uuid4)

    def id_generator(self):
        return ((self.start_time.isoformat()[0:5]) + ("-") +
                (self.end_time.isoformat()[0:5]))[0:64]

    def save(self, *args, **kwargs):
        self.c_id = self.id_generator()
        super(Bell_Timing, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('owner', 'start_time', 'end_time')
        ordering = ['start_time', 'end_time']

    def __str__(self):
        return f"On {self.name} {self.start_time} - {self.end_time}"


DAYS_OF_WEEK = {
    'Monday': 0,
    'Tuesday': 1,
    'Wednesday': 2,
    'Thursday': 3,
    'Friday': 4,
    'Saturday': 5,
    'Sunday': 6
}
DAYS = (
    ("Monday", "Monday"),
    ("Tuesday", "Tuesday"),
    ("Wednesday", "Wednesday"),
    ("Thursday", "Thursday"),
    ("Friday", "Friday"),
    ("Saturday", "Saturday"),
    ("Sunday", "Sunday")
)


class Working_Day(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=10, choices=DAYS)
    code = models.CharField(max_length=10)
    index = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    c_id = models.CharField(max_length=64, unique=True, default=uuid.uuid4)

    def id_generator(self):
        return ((self.name) + ("-") +
                (self.code) + ("-"))[0:64]

    def save(self, *args, **kwargs):
        self.c_id = self.id_generator()
        self.index = DAYS_OF_WEEK.get(self.name, "Sunday")
        super(Working_Day, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('owner', 'name',)
        ordering = ['index']

    def __str__(self):
        return f"On {self.name}"


class Time_Off(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    bell_timing = models.ForeignKey(Bell_Timing, on_delete=models.CASCADE)
    working_day = models.ForeignKey(Working_Day, on_delete=models.CASCADE)
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    c_id = models.CharField(max_length=64, unique=True, default=uuid.uuid4)

    def id_generator(self):
        return ((self.bell_timing.c_id) + ("-") +
                (self.working_day.c_id))[0:64]

    def save(self, *args, **kwargs):
        print(self)
        self.c_id = self.id_generator()
        super(Time_Off, self).save(*args, **kwargs)

    class Meta:
        unique_together = (
            'owner', 'bell_timing', 'working_day')
        ordering = ['working_day', 'bell_timing']

    def __str__(self):
        return f"{self.c_id}"


class Subject(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    c_id = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    time_off = models.ManyToManyField(Time_Off)

    def id_generator(self):
        return ((self.code) + ("-") +
                (self.name))[0:64]

    def save(self, *args, **kwargs):
        self.c_id = self.id_generator()
        super(Subject, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('owner', 'code',)
        ordering = ['code']

    def __str__(self):
        return f"{self.name} ({self.code})"


class Classroom(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    c_id = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    time_off = models.ManyToManyField(Time_Off)

    def id_generator(self):
        return ((self.code) + ("-") +
                (self.name))[0:64]

    def save(self, *args, **kwargs):
        self.c_id = self.id_generator()
        super(Classroom, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('owner', 'code',)
        ordering = ['code']

    def __str__(self):
        return f"{self.name} ({self.code})"


class Group(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    c_id = models.CharField(max_length=64, unique=True, default=uuid.uuid4)

    def id_generator(self):
        return ((self.code) + ("-") +
                (self.name))[0:64]

    def save(self, *args, **kwargs):
        self.c_id = self.id_generator()
        super(Group, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('owner', 'code')
        ordering = ['-code']

    def __str__(self):
        return f"{self.name} ({self.code})"


class Semester(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=25)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    c_id = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    time_off = models.ManyToManyField(Time_Off)
    groups = models.ManyToManyField(Group)

    def id_generator(self):
        return ((self.code) + ("-") +
                (self.name))[0:64]

    def save(self, *args, **kwargs):
        self.c_id = self.id_generator()
        super(Semester, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('owner', 'code',)
        ordering = ['code']

    def __str__(self):
        return f"{self.name} ({self.code})"


class Teacher(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=25)
    color = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    c_id = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    time_off = models.ManyToManyField(Time_Off)

    def id_generator(self):
        return ((self.code) + ("-") +
                (self.name) + ("-") +
                (self.color))[0:64]

    def save(self, *args, **kwargs):
        self.c_id = self.id_generator()
        super(Teacher, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('owner', 'code',)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Lesson(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    teachers = models.ManyToManyField(Teacher)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    lesson_per_week = models.IntegerField(default=1)
    lesson_length = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)

    def __str__(self):
        return f"{self.classroom} {self.subject}"


class SemGrpCombo(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
