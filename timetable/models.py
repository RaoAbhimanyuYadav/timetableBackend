from django.db import models
from django.contrib.auth.models import User

import uuid


class Timing(models.Model):
    owner = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)
    day = models.CharField(max_length=10)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    skip_start_time = models.TimeField(blank=True, null=True)
    skip_end_time = models.TimeField(blank=True, null=True)
    one_slot_interval = models.TimeField(blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, unique=True, editable=False)

    class Meta:
        unique_together = ('owner', 'day',)

    def __str__(self):
        return f"On {self.day}"


class Professor(models.Model):
    owner = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, blank=True, null=True)
    nick_name = models.CharField(max_length=10)
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, unique=True, editable=False)

    class Meta:
        unique_together = ('owner', 'nick_name',)

    def __str__(self):
        return f"{self.name} ({self.nick_name})"


class Year(models.Model):
    owner = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)
    semester = models.IntegerField()
    total_groups = models.IntegerField(default=1)
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, unique=True, editable=False)

    class Meta:
        unique_together = ('owner', 'semester',)

    def __str__(self):
        return f"Year:{self.semester} & total Group:{self.total_groups}"


class Subject(models.Model):
    owner = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, blank=True, null=True)
    code = models.CharField(max_length=25)
    slot_required = models.IntegerField(default=1)
    group_lecture_in_a_week = models.IntegerField(default=0)
    whole_lecture_in_a_week = models.IntegerField(default=1)
    teacher = models.ForeignKey(
        Professor, on_delete=models.CASCADE, blank=True, null=True)
    year = models.ForeignKey(
        Year, on_delete=models.CASCADE, blank=True, null=True)
    room = models.CharField(max_length=25, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, unique=True, editable=False)

    class Meta:
        unique_together = ('owner', 'code',)

    def __str__(self):
        return f"{self.name} ({self.code})"


# class Group(models.Model):
#     owner = models.ForeignKey(
#         User, blank=True, null=True, on_delete=models.CASCADE)

#     lecture_in_a_week = models.IntegerField(default=1)
#     slot_required = models.IntegerField(default=1)
#     group_number = models.IntegerField(default=1)
#     subject = models.ForeignKey(
#         Subject, on_delete=models.CASCADE, blank=True, null=True)
#     id = models.UUIDField(default=uuid.uuid4,
#                           primary_key=True, unique=True, editable=False)

#     def __str__(self):
#         return f"{self.group_number}"
# Group Number = 0 => Whole class
# Group Number = 1 => G1
# Group Number = 2 => G2
