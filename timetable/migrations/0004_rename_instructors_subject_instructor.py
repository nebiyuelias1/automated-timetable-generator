# Generated by Django 4.0.3 on 2022-03-14 18:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0003_remove_subject_instructors_subject_instructors'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subject',
            old_name='instructors',
            new_name='instructor',
        ),
    ]
