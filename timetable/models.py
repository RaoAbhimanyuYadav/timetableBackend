from django.db import models
from django.contrib.auth.models import User

import uuid


class Timing(models.Model):
    owner = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL)
    day = models.CharField(max_length=10, blank=True, null=True)
    time_from = models.TimeField(blank=True, null=True)
    time_to = models.TimeField(blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, unique=True, editable=False)

    def __str__(self):
        return f"On {self.day} from {self.time_from} to {self.time_to}"


class Professor(models.Model):
    owner = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=250, blank=True, null=True)
    nick_name = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, unique=True, editable=False)

    def __str__(self):
        return f"{self.name} ({self.nick_name})"


class Year(models.Model):
    owner = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL)
    semseter = models.IntegerField(default=1)
    room = models.CharField(max_length=25, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, unique=True, editable=False)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Subject(models.Model):
    owner = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=250, blank=True, null=True)
    code = models.CharField(max_length=25, blank=True, null=True)
    lecture_in_a_week = models.IntegerField(default=0)
    teacher = models.ForeignKey(
        Professor, on_delete=models.CASCADE, blank=True, null=True)
    year = models.ForeignKey(
        Year, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, unique=True, editable=False)

    def __str__(self):
        return f"{self.name} ({self.code})"
