from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.views.generic import ListView
from timetable.forms import SectionForm, SubjectForm

from timetable.models import Subject, Instructor, Room, Section

# Create your views here.
def index(request):
    context = {
        'subject_count': Subject.objects.count(),
        'room_count': Room.objects.count(),
        'section_count': Section.objects.count(),
        'instructor_count': Instructor.objects.count()
    }
    return render(request, 'timetable/index.html', context)

def settings(request):
    return render(request, 'timetable/settings.html')

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
    fields = ['name']
    
    def get_success_url(self):
        return reverse('instructors')

class InstructorDeleteView(DeleteView):
    model = Instructor
    success_url = reverse_lazy('instructors')
    
class InstructorUpdateView(UpdateView):
    model = Instructor
    fields = ['name']
    template_name_suffix = '_form'
    
    def get_success_url(self):
        return reverse('instructors')