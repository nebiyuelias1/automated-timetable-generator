# Generated by Django 4.0.3 on 2022-04-18 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0002_remove_instructor_subjects_instructorassignment'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduleentry',
            name='timing',
            field=models.CharField(blank=True, choices=[('BF', 'Before Noon'), ('AF', 'AFTER_NOON')], default=None, max_length=2, null=True),
        ),
    ]
