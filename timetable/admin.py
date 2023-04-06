from django.contrib import admin
from .models import (
    Bell_Timing, Classroom,  Lesson, Semester, Group, Subject, Time_Off,
    Teacher, Working_Day, SemGrpCombo
)
# Register your models here.

admin.site.register(Bell_Timing)
admin.site.register(Classroom)
admin.site.register(Lesson)
admin.site.register(Semester)
admin.site.register(Group)
admin.site.register(Time_Off)
admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(Working_Day)
admin.site.register(SemGrpCombo)
