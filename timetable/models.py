from random import randint
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


class Section(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=500)

    grade = models.ForeignKey(Grade, related_name='sections',
                              null=False, blank=False, on_delete=models.CASCADE)

    room = models.ForeignKey(Room, related_name='sections',
                             null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'Grade: {self.grade} Section: {self.name}'


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

    flexibility = models.CharField(max_length=2,
                                   choices=FLEXIBILITY_OPTIONS,
                                   default=FLEXIBLE,
                                   null=False,
                                   blank=False)

    def __str__(self) -> str:
        return self.name


class InstructorAssignment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    instructor = models.ForeignKey(
        Instructor, related_name='assignments', null=False, blank=False, on_delete=models.CASCADE)

    subject = models.ForeignKey(
        Subject, related_name='instructors', null=False, blank=False, on_delete=models.CASCADE)

    section = models.ForeignKey(
        Section, related_name='instructors', null=False, blank=False, on_delete=models.CASCADE)


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

    def add_schedule_entry(self, day, period, subject, timing):
        self.__entries.append(ScheduleEntry(
            day=self.__days[day-1], period=period, subject=subject, timing=timing))

    def save_schedule_entries(self):
        for day in self.__days:
            day.save()

        ScheduleEntry.objects.bulk_create(self.__entries)
        
    def swap_day_schedule(self, day_one, day_two):
        temp = self.__days[day_one - 1]
        self.__days[day_one - 1].day = day_two
        self.__days[day_one - 1] = self.__days[day_two - 1]
        self.__days[day_two - 1] = temp
        self.__days[day_two - 1].day = day_one

    def calculate_fitness(self):
        num_of_conflicts = 0
        for entry in self.__entries:
            instructor = entry.subject.instructors.filter(section=entry.day.schedule.section).first().instructor

            instructor_conflict_exists = ScheduleEntry.objects.filter(
                day__day=entry.day.day, period=entry.period, subject__instructors__instructor__in=[instructor.id]).exists()
            
            if instructor_conflict_exists:
                num_of_conflicts += 1
                
            if instructor.flexibility == Instructor.MORNING and entry.timing == ScheduleEntry.AFTER_NOON:
                num_of_conflicts += 0.01
            elif instructor.flexibility == Instructor.AFTERNOON and entry.timing == ScheduleEntry.BEFORE_NOON:
                num_of_conflicts += 0.01

        self.__fitness = 1 / (num_of_conflicts + 1)
        
    def mutate(self):
        random_index = randint(1, len(self.__entries)-1)
        temp_day = self.__entries[random_index].day
        temp_period = self.__entries[random_index].period
        
        self.__entries[random_index].day = self.__entries[random_index - 1].day
        self.__entries[random_index].period = self.__entries[random_index - 1].period
        
        self.__entries[random_index - 1].day = temp_day
        self.__entries[random_index - 1].period = temp_period


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
    BEFORE_NOON = 'BF'
    AFTER_NOON = 'AF'
    
    TIMING_OPTIONS = (
        (BEFORE_NOON, 'Before Noon'),
        (AFTER_NOON, 'AFTER_NOON'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    day = models.ForeignKey(DaySchedule, related_name='entries',
                            null=True, blank=True, on_delete=models.CASCADE)

    period = models.IntegerField()

    subject = models.ForeignKey(
        Subject, related_name='+', blank=True, null=True, on_delete=models.SET_NULL)
    
    timing = models.CharField(choices=TIMING_OPTIONS, default=None, null=True, blank=True, max_length=2)

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
