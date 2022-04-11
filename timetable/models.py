import uuid
from django.db import models


class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=500)

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

    grade = models.ForeignKey(Grade, related_name='subjects',
                              blank=False, null=False, on_delete=models.CASCADE)

    number_of_occurrences = models.IntegerField()

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

    subjects = models.ManyToManyField(Subject, related_name='instructors')

    availability = models.DurationField()

    flexibility = models.CharField(max_length=2,
                                   choices=FLEXIBILITY_OPTIONS,
                                   default=FLEXIBLE,
                                   null=False,
                                   blank=False)

    def __str__(self) -> str:
        return self.name


class Section(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=500)

    grade = models.ForeignKey(Grade, related_name='sections',
                              null=False, blank=False, on_delete=models.CASCADE)

    room = models.ForeignKey(Room, related_name='sections',
                             null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'Grade: {self.grade} Section: {self.name}'


class Schedule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    section = models.ForeignKey(
        Section, related_name='schedule', blank=False, null=False, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__entries = []
        self.__fitness = 1
        self.__days = []
        for i in range(1, 6):
            self.__days.append(DaySchedule(day=i, schedule=self))
    
    @property
    def fitness(self):
        return self.__fitness
        

    def add_schedule_entry(self, day, period, subject):
        self.__entries.append(ScheduleEntry(day=self.__days[day-1], period=period, subject=subject))
        
    def save_schedule_entries(self):
        for day in self.__days:
            day.save()
            
        ScheduleEntry.objects.bulk_create(self.__entries)

    def calculate_fitness(self):
        num_of_conflicts = 0
        for entry in self.__entries:
            instructor_id = entry.subject.instructors.first().id

            instructor_conflict_exists = ScheduleEntry.objects.filter(
                day__day=entry.day.day, period=entry.period, subject__instructors__in=[instructor_id]).exists()
            
            if instructor_conflict_exists:
                num_of_conflicts += 1
                
        self.__fitness = 1 / (num_of_conflicts + 1)
        
        
class DaySchedule(models.Model):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    
    DAYS_OF_THE_WEEK = (
        (MONDAY, 'Monday'),
        (TUESDAY, 'Tuesday'),
        (WEDNESDAY, 'Wednesday'),
        (THURSDAY, 'Thursday'),
        (FRIDAY, 'Friday'),
    )
    
    schedule = models.ForeignKey(
        Schedule, related_name='days', null=False, blank=False, on_delete=models.CASCADE)
    
    day = models.IntegerField(choices=DAYS_OF_THE_WEEK)

class ScheduleEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    day = models.ForeignKey(DaySchedule, related_name='entries', null=True, blank=True, on_delete=models.CASCADE)

    period = models.IntegerField()

    subject = models.ForeignKey(
        Subject, related_name='+', blank=True, null=True, on_delete=models.SET_NULL)
    
    def __str__(self) -> str:
        return f'{self.subject}'


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

    setting = models.ForeignKey(
        Setting, null=False, blank=False, on_delete=models.CASCADE, related_name='breaks')
