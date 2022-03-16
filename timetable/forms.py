from django.forms import ModelForm

from timetable.models import Grade, Section, Subject

class GradeForm(ModelForm):
    class Meta:
        model = Grade
        fields = ['level',]
class SectionForm(ModelForm):
    class Meta:
        model = Section
        fields = ['name', 'grade']
        
class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'grade', 'instructor']