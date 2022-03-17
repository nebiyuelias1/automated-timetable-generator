import datetime
from typing import Any, Mapping, Optional
from django.forms import DurationField, Form, ModelForm, TimeField, TimeInput, ValidationError
from durationwidget.widgets import TimeDurationWidget


from timetable.models import Grade, Section, Subject


class GradeForm(ModelForm):
    class Meta:
        model = Grade
        fields = ['level', ]


class SectionForm(ModelForm):
    class Meta:
        model = Section
        fields = ['name', 'grade', 'room']


class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'grade', 'instructor']


class SettingForm(Form):
    class_start_time = TimeField(widget=TimeInput(attrs={'type': 'time'}))

    class_end_time = TimeField(widget=TimeInput(attrs={'type': 'time'}))

    period_length = DurationField(widget=TimeDurationWidget(
        show_days=False, show_hours=False,  show_seconds=False))

    lunch_start_time = TimeField(widget=TimeInput(attrs={'type': 'time'}))

    lunch_end_time = TimeField(widget=TimeInput(attrs={'type': 'time'}))

    def clean(self) -> Optional[Mapping[str, Any]]:
        cleaned_data = super().clean()
        start_time = cleaned_data.get('class_start_time')
        end_time = cleaned_data.get('class_end_time')
        if start_time >= end_time:
            self.add_error('class_end_time',
                           'End time must be after start time.')

        lunch_start_time = cleaned_data.get('lunch_start_time')
        lunch_end_time = cleaned_data.get('lunch_end_time')
        if lunch_start_time >= lunch_end_time:
            self.add_error('lunch_end_time',
                           'Lunch end time must be after start time.')

        day_duration = self._get_duration_in_seconds(start_time, end_time)
        lunch_duration = self._get_duration_in_seconds(
            lunch_start_time, lunch_end_time)
        class_duration = day_duration - lunch_duration
        period_length = cleaned_data.get('period_length').total_seconds()
        number_of_periods = class_duration / period_length
        if number_of_periods != int(number_of_periods):
            raise ValidationError(
                'It\'s not possible to have equally spaced periods with current configuration. Please adjust!', code='invalid')

        return cleaned_data

    def _get_duration_in_seconds(self, start_time, end_time):
        start_time = datetime.datetime.combine(
            datetime.date(2022, 3, 17), start_time)
        end_time = datetime.datetime.combine(
            datetime.date(2022, 3, 17), end_time)
        return (end_time - start_time).total_seconds()
