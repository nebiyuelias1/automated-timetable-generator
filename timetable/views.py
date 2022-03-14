from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.views.generic import ListView

from timetable.models import Subject, Instructor, Room, Section

# Create your views here.
def index(request):
    return render(request, 'timetable/index.html')

def sections(request):
    return render(request, 'timetable/sections.html')

def classes(request):
    return render(request, 'timetable/classes.html')

def instructors(request):
    return render(request, 'timetable/instructors.html')

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
    fields = ['name']
    
    def get_success_url(self):
        return reverse('subjects')

class SubjectDeleteView(DeleteView):
    model = Subject
    success_url = reverse_lazy('subjects')
    
class SubjectUpdateView(UpdateView):
    model = Subject
    fields = ['name']
    template_name_suffix = '_form'
    
    def get_success_url(self):
        return reverse('subjects')
    
class SectionListView(ListView):
    model = Section
    paginate_by = 10
    
class SectionCreateView(CreateView):
    model = Section
    fields = ['name']
    
    def get_success_url(self):
        return reverse('sections')

class SectionDeleteView(DeleteView):
    model = Section
    success_url = reverse_lazy('sections')
    
class SectionUpdateView(UpdateView):
    model = Section
    fields = ['name']
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