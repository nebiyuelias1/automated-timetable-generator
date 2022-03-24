import uuid
from django.db import models

class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=500)
    
    def __str__(self) -> str:
        return self.name

class Instructor(models.Model):
    FLEXIBLE = 'FL'
    MORNING = 'MR'
    AFTERNOON = 'AF'
    
    FLEXIBILITY_OPTIONS = (
        (FLEXIBLE, 'Flexible'),
        (MORNING, 'Morning'),
        (AFTERNOON, 'Afternoon')
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=500)
    
    availability = models.DurationField()
    
    flexibility = models.CharField(max_length=2, choices=FLEXIBILITY_OPTIONS, default=FLEXIBLE, null=False, blank=False)
    
    def __str__(self) -> str:
        return self.name

class Grade(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    level = models.CharField(max_length=50, null=False, blank=False)
    
    def __str__(self) -> str:
        return f'G-{self.level}'
    
class Subject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=500)
    
    grade = models.ForeignKey(Grade, related_name='subjects', blank=False, null=False, on_delete=models.CASCADE)
    
    instructor = models.ForeignKey(Instructor, related_name='subjects', blank=True, null=True, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.name


    
class Section(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=500)
    
    grade = models.ForeignKey(Grade, related_name='sections', null=False, blank=False, on_delete=models.CASCADE)
    
    room = models.ForeignKey(Room, related_name='sections', null=False, blank=False, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f'Grade: {self.grade} Section: {self.name}'
    
class Schedule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    section = models.ForeignKey(Section, related_name='schedule', blank=False, null=False, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
class ScheduleEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    day = models.IntegerField()
    
    period = models.IntegerField()
    
    schedule = models.ForeignKey(Schedule, related_name='entries', null=False, blank=False, on_delete=models.CASCADE)
    
class Setting(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    start_time = models.TimeField()
    
    end_time = models.TimeField()
    
    lunch_start_time = models.TimeField()
    
    lunch_end_time = models.TimeField()
    
    period_length = models.DurationField()
    
    before_lunch_period_count = models.IntegerField()
    
    after_lunch_period_count = models.IntegerField()
    
class Break(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    start_time = models.TimeField()
    
    end_time = models.TimeField()
    
    setting = models.ForeignKey(Setting, null=False, blank=False, on_delete=models.CASCADE, related_name='breaks')

    


