# Generated by Django 4.1.2 on 2022-10-29 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0005_alter_year_semseter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='year',
            name='semseter',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
