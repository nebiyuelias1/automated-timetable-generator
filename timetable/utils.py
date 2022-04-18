import datetime
from functools import reduce
import random

from django.conf import settings

from timetable.models import Schedule, ScheduleEntry, Section, Setting


def get_duration_in_seconds(start_time, end_time):
    start_time = datetime.datetime.combine(
        datetime.date(2022, 3, 17), start_time)
    end_time = datetime.datetime.combine(
        datetime.date(2022, 3, 17), end_time)
    return (end_time - start_time).total_seconds()


def _initialize_population(section: Section, before_lunch_period_count, after_lunch_period_count):
    population = []
    all_subjects = section.grade.subjects.all()
    
    for _ in range(settings.POPULATION_SIZE):
        schedule = Schedule(section=section)
        period_allocation_map = {i: set() for i in range(1, 6)}
        
        for subject in all_subjects:
            number_of_occurrences = subject.number_of_occurrences
            while number_of_occurrences > 0:
                rand_day = random.randint(1, 5)
                rand_period = random.randint(1, before_lunch_period_count + after_lunch_period_count)
                if rand_period in period_allocation_map[rand_day]:
                    continue
                timing = ScheduleEntry.AFTER_NOON if rand_period > before_lunch_period_count else ScheduleEntry.BEFORE_NOON
                
                schedule.add_schedule_entry(day=rand_day, period=rand_period, subject=subject, timing=timing)
                number_of_occurrences -= 1
                period_allocation_map[rand_day].add(rand_period)
        
        schedule.calculate_fitness()
        population.append(schedule)
        
    return population

def _create_next_generation(mating_pool):
    next_generation = []
    
    mating_pool_size = len(mating_pool)
    for _ in range(settings.POPULATION_SIZE):
        a = random.randint(0, mating_pool_size - 1)
        b = random.randint(0, mating_pool_size - 1)
        
        parent_a = mating_pool[a]
        parent_b = mating_pool[b]
        
        if parent_a.fitness > parent_b.fitness:
            next_generation.append(parent_a)
        else:
            next_generation.append(parent_b)
            
    return next_generation
    
def _natural_selection(population):
    mating_pool = []
    
    fitness_sum = reduce(lambda x,y: x + y.fitness, population, 0.0)
    
    for item in population:
        normalized_fitness = int((item.fitness * 100 / fitness_sum) * settings.POPULATION_SIZE)
        mating_pool += ([item] * normalized_fitness)
        
    return _create_next_generation(mating_pool)
        

def auto_generate_schedule():
    # get settings
    setting = Setting.objects.first()
    before_lunch_period_count = setting.before_lunch_period_count
    after_lunch_period_count = setting.after_lunch_period_count

    # Get all sections from database
    sections = Section.objects.all()

    # for each section
    for section in sections:
        population = _initialize_population(section,
                               before_lunch_period_count=before_lunch_period_count,
                               after_lunch_period_count=after_lunch_period_count)
        
        while True:
            population = _natural_selection(population)
            
            found_solution = True in (i.fitness > 0.1 for i in population)
            
            if found_solution:
                break
            
        population.sort(key=lambda x: x.fitness, reverse=True)
        best_schedule = population[0]
        best_schedule.save()
        best_schedule.save_schedule_entries()
