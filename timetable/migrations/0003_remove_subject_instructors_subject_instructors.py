# Generated by Django 4.0.3 on 2022-03-14 18:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0002_auto_20220314_1820'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subject',
            name='instructors',
        ),
        migrations.AddField(
            model_name='subject',
            name='instructors',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subjects', to='timetable.instructor'),
        ),
    ]
