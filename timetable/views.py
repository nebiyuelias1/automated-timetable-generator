from datetime import datetime, timedelta
from typing import Any, Dict, List
from django.forms import ValidationError, formset_factory
from django.db.models import Count, F, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.views.generic import ListView
from timetable.forms import BreakForm, GradeForm, InstructorAssignmentForm, InstructorForm, SectionForm, SettingForm, SubjectForm

from timetable.models import Grade, InstructorAssignment, Schedule, ScheduleEntry, Setting, Subject, Instructor, Room, Section, Break
from timetable.utils import auto_generate_schedule, get_duration_in_seconds

# Create your views here.


def index(request):
    setting = Setting.objects.first()
    period_length = setting.period_length if setting else 0
    period_length = period_length / 60

    has_unassigned_instructors = Subject.objects.annotate(
        instructor_count=Count('instructors')).filter(Q(instructor_count=0)).exists()
    disable_generate_button = has_unassigned_instructors

    context = {
        'subject_count': Subject.objects.count(),
        'room_count': Room.objects.count(),
        'section_count': Section.objects.count(),
        'instructor_count': Instructor.objects.count(),
        'schedule_count': Schedule.objects.count(),
        'has_unassigned_instructors': has_unassigned_instructors,
        'disable_generate_button': disable_generate_button
    }
    return render(request, 'timetable/index.html', context)


def get_breaks_data(form_data, break_count):
    data = {}
    for i in range(break_count):
        start_time_key = f'form-{i}-start_time'
        end_time_key = f'form-{i}-end_time'
        data[start_time_key] = form_data.get(start_time_key)
        data[end_time_key] = form_data.get(end_time_key)
    return data


def settings(request):
    setting = Setting.objects.all().first()
    if setting:
        return render(request, 'timetable/setting_display.html', {'setting': setting})

    break_count = int(request.GET.get('break', 0))
    BreakFormSet = formset_factory(BreakForm, extra=break_count)

    if request.method == 'POST':
        form = SettingForm(request.POST)
        break_form_set = BreakFormSet({
            **get_breaks_data(request.POST, break_count),
            'form-TOTAL_FORMS': f'{break_count}',
            'form-INITIAL_FORMS': f'{break_count}',
        })

        if form.is_valid() and break_form_set.is_valid():
            setting_data = form.cleaned_data
            before_lunch_duration = get_duration_in_seconds(
                setting_data['start_time'], setting_data['lunch_start_time'],
            )
            after_lunch_duration = get_duration_in_seconds(
                setting_data['lunch_end_time'], setting_data['end_time'],
            )

            for break_form in break_form_set:
                if break_form.cleaned_data['start_time'] < setting_data['lunch_start_time']:
                    before_lunch_duration -= get_duration_in_seconds(
                        break_form.cleaned_data['start_time'], break_form.cleaned_data['end_time'])
                elif break_form.cleaned_data['start_time'] > setting_data['lunch_end_time']:
                    after_lunch_duration -= get_duration_in_seconds(
                        break_form.cleaned_data['start_time'], break_form.cleaned_data['end_time'])

            period_length = setting_data['period_length'].total_seconds()

            before_lunch_number_of_periods = before_lunch_duration / period_length
            if before_lunch_number_of_periods != int(before_lunch_number_of_periods):
                raise ValidationError(
                    'It\'s not possible to have equally spaced periods with current configuration. Please adjust!', code='invalid')
            after_lunch_number_of_periods = after_lunch_duration / period_length
            if after_lunch_number_of_periods != int(after_lunch_number_of_periods):
                raise ValidationError(
                    'It\'s not possible to have equally spaced periods with current configuration. Please adjust!', code='invalid')

            setting = Setting.objects.create(**form.cleaned_data,
                                             before_lunch_period_count=before_lunch_number_of_periods,
                                             after_lunch_period_count=after_lunch_number_of_periods)
            for break_form in break_form_set:
                Break.objects.create(
                    **break_form.cleaned_data, setting=setting)

            return render(request, 'timetable/setting_display.html', {'setting': setting})

    form = SettingForm()
    return render(request, 'timetable/setting_form.html', {'form': form, 'break_count': break_count + 1, 'break_form_set': BreakFormSet(), })


def subjects_in_grade(request, pk):
    subjects = Subject.objects.filter(grade=pk)

    return render(request, 'timetable/subjects_drop_down_list_options.html', {'subjects': subjects})


def edit_setting(request):
    setting_queryset = Setting.objects.all()
    break_count = int(request.GET.get(
        'break', setting_queryset.first().breaks.count()))
    BreakFormSet = formset_factory(BreakForm, extra=break_count)

    if request.method == 'POST':
        form = SettingForm(request.POST)
        data = get_breaks_data(request.POST, break_count)

        break_form_set = BreakFormSet({
            **data,
            'form-TOTAL_FORMS': f'{break_count}',
            'form-INITIAL_FORMS': f'{break_count}'})

        if form.is_valid() and break_form_set.is_valid():
            setting_queryset.update(**form.cleaned_data)
            if break_count > 0:
                setting_queryset.first().breaks.all().delete()
                for break_form in break_form_set:
                    Break.objects.create(**break_form.cleaned_data,
                                         setting=setting_queryset.first())
        else:
            return render(request, 'timetable/setting_form.html', {'form': form,
                                                                   'break_form_set': break_form_set,
                                                                   'break_count': break_count + 1, })

        return redirect(reverse('settings'))

    if setting_queryset.count() > 0:
        setting_queryset = setting_queryset.first()
        data = {
            'start_time': str(setting_queryset.start_time),
            'end_time': str(setting_queryset.end_time),
            'lunch_start_time': str(setting_queryset.lunch_start_time),
            'lunch_end_time': str(setting_queryset.lunch_end_time),
            'period_length_0': setting_queryset.period_length.total_seconds() / 60,
        }
        form = SettingForm(data)

        return render(request, 'timetable/setting_form.html', {'form': form,
                                                               'break_form_set': BreakFormSet(),
                                                               'break_count': break_count + 1, })

    raise ValidationError('Nothing to edit!')


def generate_schedule(request):
    auto_generate_schedule()
    return redirect(reverse('index'))


def _get_timetable(total_periods, entries: List[ScheduleEntry]):
    timetable = {i: {j: None for j in range(
        1, total_periods + 1)} for i in range(1, 6)}

    for entry in entries:
        day = entry.day.day
        period = entry.period
        timetable[day][period] = entry

    return timetable


def _get_periods(setting: Setting):
    periods = []

    period_length_in_minutes = setting.period_length.total_seconds() / 60

    start_time_datetime = datetime(
        2022, 4, 11, setting.start_time.hour, setting.start_time.minute)

    for i in range(setting.before_lunch_period_count):
        start_time = start_time_datetime + \
            timedelta(minutes=period_length_in_minutes * i)
        end_time = start_time + timedelta(minutes=period_length_in_minutes)
        periods.append([start_time, end_time])

    start_time_datetime = datetime(
        2022, 4, 11, setting.lunch_end_time.hour, setting.lunch_end_time.minute)
    for i in range(setting.after_lunch_period_count):
        start_time = start_time_datetime + \
            timedelta(minutes=period_length_in_minutes * i)
        end_time = start_time + timedelta(minutes=period_length_in_minutes)
        periods.append([start_time, end_time])

    return periods


def display_schedule(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk)
    setting = Setting.objects.first()
    total_periods = setting.before_lunch_period_count + \
        setting.after_lunch_period_count

    schedule_entries = ScheduleEntry.objects.filter(day__schedule=schedule).order_by(
        'day__day', 'period').select_related('subject')
    timetable = _get_timetable(
        total_periods=total_periods, entries=schedule_entries)
    periods = _get_periods(setting)

    return render(request, 'timetable/schedule_display.html', {'setting': setting,
                                                               'schedule': schedule,
                                                               'periods': periods,
                                                               'timetable': timetable,
                                                               'period_range': range(1, total_periods + 1),
                                                               'day_range': range(1, 6)})


class ScheduleListView(ListView):
    model = Schedule
    paginate_by = 10


class GradeListView(ListView):
    model = Grade
    paginate_by = 10


class GradeCreateView(CreateView):
    model = Grade
    form_class = GradeForm

    def get_success_url(self):
        return reverse('grades')


class GradeDeleteView(DeleteView):
    model = Grade
    success_url = reverse_lazy('grades')


class GradeUpdateView(UpdateView):
    model = Grade
    form_class = GradeForm
    template_name_suffix = '_form'

    def get_success_url(self):
        return reverse('grades')


class RoomListView(ListView):
    model = Room
    paginate_by = 10


class RoomCreateView(CreateView):
    model = Room
    fields = ['name']

    def get_success_url(self):
        return reverse('rooms')


class RoomDeleteView(DeleteView):
    model = Room
    success_url = reverse_lazy('rooms')


class RoomUpdateView(UpdateView):
    model = Room
    fields = ['name']
    template_name_suffix = '_form'

    def get_success_url(self):
        return reverse('rooms')


class SubjectListView(ListView):
    model = Subject
    paginate_by = 10


class SubjectCreateView(CreateView):
    model = Subject
    form_class = SubjectForm

    def get_success_url(self):
        return reverse('subjects')


class SubjectDeleteView(DeleteView):
    model = Subject
    success_url = reverse_lazy('subjects')


class SubjectUpdateView(UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name_suffix = '_form'

    def get_success_url(self):
        return reverse('subjects')


class SectionListView(ListView):
    model = Section
    paginate_by = 10


class SectionCreateView(CreateView):
    model = Section
    form_class = SectionForm

    def get_success_url(self):
        return reverse('sections')


class SectionDeleteView(DeleteView):
    model = Section
    success_url = reverse_lazy('sections')


class SectionUpdateView(UpdateView):
    model = Section
    form_class = SectionForm
    template_name_suffix = '_form'

    def get_success_url(self):
        return reverse('sections')


class InstructorListView(ListView):
    model = Instructor
    paginate_by = 10


class InstructorCreateView(CreateView):
    model = Instructor
    form_class = InstructorForm

    def get_success_url(self):
        return reverse('instructors')


class InstructorDeleteView(DeleteView):
    model = Instructor
    success_url = reverse_lazy('instructors')


class InstructorUpdateView(UpdateView):
    model = Instructor
    form_class = InstructorForm
    template_name_suffix = '_form'

    def get_success_url(self):
        return reverse('instructors')


def instructor_assignment_list_view(request):
    context = {
        'sections': Section.objects.all()
    }
    
    return render(request, 'timetable/instructorassignment_list.html', context=context)

class InstructorAssignmentCreateView(CreateView):
    model = InstructorAssignment
    form_class = InstructorAssignmentForm

    def get_success_url(self):
        return reverse('instructor-assignments')
    
    def get_initial(self) -> Dict[str, Any]:
        initial = super().get_initial()
        
        section_id = self.request.GET.get('section_id')
        subject_id = self.request.GET.get('subject_id')
        section = get_object_or_404(Section, pk=section_id)
        subject = get_object_or_404(Subject, pk=subject_id)
        
        initial['subject'] = subject
        initial['section'] = section
        
        return initial
    

class InstructorAssignmentUpdateView(UpdateView):
    model = InstructorAssignment
    form_class = InstructorAssignmentForm

    def get_success_url(self):
        return reverse('instructor-assignments')