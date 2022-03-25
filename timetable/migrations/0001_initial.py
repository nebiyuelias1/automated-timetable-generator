# Generated by Django 4.0.3 on 2022-03-25 18:52

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('level', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('lunch_start_time', models.TimeField()),
                ('lunch_end_time', models.TimeField()),
                ('period_length', models.DurationField()),
                ('before_lunch_period_count', models.IntegerField()),
                ('after_lunch_period_count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=500)),
                ('number_of_occurrences', models.IntegerField()),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subjects', to='timetable.grade')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=500)),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='timetable.grade')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='timetable.room')),
            ],
        ),
        migrations.CreateModel(
            name='ScheduleEntry',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('day', models.IntegerField()),
                ('period', models.IntegerField()),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='timetable.schedule')),
            ],
        ),
        migrations.AddField(
            model_name='schedule',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedule', to='timetable.section'),
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=500)),
                ('availability', models.DurationField()),
                ('flexibility', models.CharField(choices=[('FL', 'Flexible'), ('MR', 'Morning'), ('AF', 'Afternoon')], default='FL', max_length=2)),
                ('subjects', models.ManyToManyField(related_name='instructors', to='timetable.subject')),
            ],
        ),
        migrations.CreateModel(
            name='Break',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('setting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='breaks', to='timetable.setting')),
            ],
        ),
    ]
