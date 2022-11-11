from django.contrib import admin
from .models import Timing, Professor, Year, Subject, Group
# Register your models here.

admin.site.register(Timing)
admin.site.register(Professor)
admin.site.register(Year)
admin.site.register(Subject)
admin.site.register(Group)
