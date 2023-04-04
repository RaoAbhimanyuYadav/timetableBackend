from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Working_Day, Bell_Timing, Time_Off


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
