from django.forms import ModelForm

from timetable.models import Section, Subject

class SectionForm(ModelForm):
    class Meta:
        model = Section
        fields = ['name', 'grade']
        
class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'grade', 'instructor']