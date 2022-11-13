# Generated by Django 4.1.2 on 2022-11-13 08:35

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('timetable', '0013_subject_group_lecture_in_a_week_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professor',
            name='nick_name',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='subject',
            name='code',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='timing',
            name='day',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='year',
            name='semester',
            field=models.IntegerField(),
        ),
        migrations.AlterUniqueTogether(
            name='professor',
            unique_together={('owner', 'nick_name')},
        ),
        migrations.AlterUniqueTogether(
            name='subject',
            unique_together={('owner', 'code')},
        ),
        migrations.AlterUniqueTogether(
            name='timing',
            unique_together={('owner', 'day')},
        ),
        migrations.AlterUniqueTogether(
            name='year',
            unique_together={('owner', 'semester')},
        ),
    ]
