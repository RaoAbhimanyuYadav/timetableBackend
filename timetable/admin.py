from django.contrib import admin
from .models import (Bell_Timing, Classroom, Classroom_Time_Off, Lesson, Semester, Semester_Group,
                     Semester_Time_Off, Subject, Subject_Time_Off,
                     Teacher, Teacher_Time_Off, Working_Day)
# Register your models here.

admin.site.register(Bell_Timing)
admin.site.register(Classroom)
admin.site.register(Classroom_Time_Off)
admin.site.register(Lesson)
admin.site.register(Semester)
admin.site.register(Semester_Group)
admin.site.register(Semester_Time_Off)
admin.site.register(Subject)
admin.site.register(Subject_Time_Off)
admin.site.register(Teacher)
admin.site.register(Teacher_Time_Off)
admin.site.register(Working_Day)
