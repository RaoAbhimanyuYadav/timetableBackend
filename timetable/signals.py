from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Working_Day, Bell_Timing, Time_Off, Group
from django.contrib.auth.models import User
from api.serializers import BellTimingSerializer


@receiver(post_save, sender=Working_Day)
def save_time_off(sender, instance, created, **kwargs):
    if (created):
        timings = Bell_Timing.objects.all()
        for timing in timings:
            tOff = Time_Off.objects.create(
                bell_timing=timing, working_day=instance, owner=instance.owner)
            tOff.save()


@receiver(post_save, sender=Bell_Timing)
def save_day_time_off(sender, instance, created, **kwargs):
    if (created):
        days = Working_Day.objects.all()
        for day in days:
            tOff = Time_Off.objects.create(
                bell_timing=instance, working_day=day, owner=instance.owner)
            tOff.save()


DAYS_OF_WEEK = (
    ("Monday", "Mon"),
    ("Tuesday", "Tue"),
    ("Wednesday", "Wed"),
    ("Thursday", "Thu"),
    ("Friday", "Fri"),
)
TIMINGS = (
    {"start_time": "08:00", "end_time": "09:00", "name": "1"},
    {"start_time": "09:00", "end_time": "10:00", "name": "2"},
    {"start_time": "10:00", "end_time": "11:00", "name": "3"},
    {"start_time": "11:00", "end_time": "12:00", "name": "4"},
    {"start_time": "12:00", "end_time": "13:00", "name": "5"},
    {"start_time": "13:00", "end_time": "14:00", "name": "6"},
    {"start_time": "14:00", "end_time": "15:00", "name": "7"},
    {"start_time": "15:00", "end_time": "16:00", "name": "8"},
    {"start_time": "16:00", "end_time": "17:00", "name": "9"},
    {"start_time": "17:00", "end_time": "18:00", "name": "10"},
)

GROUPS = (
    ("Whole", "W"),
    ("Group 1", "G1"),
    ("Group 2", "G2"),
    ("Group 3", "G3"),
)


@receiver(post_save, sender=User)
def basic_info(sender, instance, created, **kwargs):
    if (created):
        for day, code in DAYS_OF_WEEK:
            Working_Day.objects.create(code=code, owner=instance, name=day)
        for data in TIMINGS:
            serializer = BellTimingSerializer(data=data)
            if serializer.is_valid():
                serializer.save(owner=instance)
        for name, code in GROUPS:
            Group.objects.create(owner=instance, name=name, code=code)
