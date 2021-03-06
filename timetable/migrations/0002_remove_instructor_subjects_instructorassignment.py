# Generated by Django 4.0.3 on 2022-04-16 09:16

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instructor',
            name='subjects',
        ),
        migrations.CreateModel(
            name='InstructorAssignment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='timetable.instructor')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instructors', to='timetable.section')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instructors', to='timetable.subject')),
            ],
        ),
    ]
