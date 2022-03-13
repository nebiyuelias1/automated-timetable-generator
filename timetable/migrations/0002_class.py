# Generated by Django 4.0.3 on 2022-03-13 11:14

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=500)),
            ],
        ),
    ]
