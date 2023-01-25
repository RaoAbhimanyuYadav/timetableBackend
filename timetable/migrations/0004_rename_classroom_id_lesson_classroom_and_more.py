# Generated by Django 4.1.5 on 2023-01-25 22:09

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('timetable', '0003_rename_bell_timing_id_classroom_time_off_bell_timing_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lesson',
            old_name='classroom_id',
            new_name='classroom',
        ),
        migrations.RenameField(
            model_name='lesson',
            old_name='semester_id',
            new_name='semester',
        ),
        migrations.RenameField(
            model_name='lesson',
            old_name='semester_group_id',
            new_name='semester_group',
        ),
        migrations.RenameField(
            model_name='lesson',
            old_name='subject_id',
            new_name='subject',
        ),
        migrations.RenameField(
            model_name='lesson',
            old_name='teacher_id',
            new_name='teacher',
        ),
        migrations.AlterUniqueTogether(
            name='lesson',
            unique_together={('owner', 'lesson_per_week', 'classroom', 'subject', 'semester', 'semester_group')},
        ),
    ]
