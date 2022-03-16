from django.forms import Form, ModelForm, TimeField, TimeInput

from timetable.models import Grade, Section, Subject

class GradeForm(ModelForm):
    class Meta:
        model = Grade
        fields = ['level',]
class SectionForm(ModelForm):
    class Meta:
        model = Section
        fields = ['name', 'grade', 'room']
        
class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'grade', 'instructor']
        
class SettingForm(Form):
    start_time = TimeField(widget=TimeInput(attrs={'type': 'time'}))
    
    end_time = TimeField(widget=TimeInput(attrs={'type': 'time'}))