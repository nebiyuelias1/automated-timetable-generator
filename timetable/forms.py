from typing import Any, Dict, Mapping, Optional
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.forms import DurationField, Form, ModelForm, TimeField, TimeInput
from durationwidget.widgets import TimeDurationWidget


from timetable.models import Break, Grade, Instructor, InstructorAssignment, Section, Setting, Subject


class GradeForm(ModelForm):
    class Meta:
        model = Grade
        fields = ('level', )


class InstructorForm(ModelForm):
    
    class Meta:
        model = Instructor
        fields = ('name', 'availability', 'flexibility')
        widgets = {
            'availability': TimeDurationWidget(
                show_days=False,
                show_hours=True,
                show_minutes=False,
                show_seconds=False,
            ),
        }

class InstructorAssignmentForm(ModelForm):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = InstructorAssignment
        fields = ('subject', 'section', 'instructor')
        
    def clean(self) -> Optional[Dict[str, Any]]:
        setting = Setting.objects.first()
        period_length = setting.period_length.total_seconds() if setting else 0
        
        cleaned_data = super().clean()
        instructor = cleaned_data.get('instructor')
        subject = cleaned_data.get('subject')
        subject_period_length = subject.number_of_occurrences * period_length
        
        total_occurrences = InstructorAssignment.objects.filter(instructor=instructor).aggregate(total_occurrences=Coalesce(Sum('subject__number_of_occurrences'), 0))['total_occurrences']
        total_occurrences = total_occurrences * period_length
        total_occurrences += subject_period_length
        
        instructor_availability = instructor.availability.total_seconds()
        if total_occurrences > instructor_availability:
            self.add_error(None, 'More than the instructor\'s availability hours per week.')
        
        return cleaned_data

class SectionForm(ModelForm):
    class Meta:
        model = Section
        fields = ['name', 'grade', 'room']


class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'grade', 'number_of_occurrences', ]


class BreakForm(ModelForm):
    class Meta:
        fields = ['start_time', 'end_time']
        model = Break
        widgets = {
            'start_time': TimeInput(attrs={'type': 'time'}),
            'end_time': TimeInput(attrs={'type': 'time'})
        }

    def clean(self) -> Optional[Mapping[str, Any]]:
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        if start_time >= end_time:
            self.add_error(None, 'End time must be after start time.')
            
        return cleaned_data


class SettingForm(Form):
    start_time = TimeField(widget=TimeInput(attrs={'type': 'time'}))

    end_time = TimeField(widget=TimeInput(attrs={'type': 'time'}))

    period_length = DurationField(widget=TimeDurationWidget(
        show_days=False, show_hours=False,  show_seconds=False))

    lunch_start_time = TimeField(widget=TimeInput(attrs={'type': 'time'}))

    lunch_end_time = TimeField(widget=TimeInput(attrs={'type': 'time'}))

    def clean(self) -> Optional[Mapping[str, Any]]:
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        if start_time >= end_time:
            self.add_error('end_time',
                           'End time must be after start time.')

        lunch_start_time = cleaned_data.get('lunch_start_time')
        lunch_end_time = cleaned_data.get('lunch_end_time')
        if lunch_start_time >= lunch_end_time:
            self.add_error('lunch_end_time',
                           'Lunch end time must be after start time.')

        return cleaned_data
