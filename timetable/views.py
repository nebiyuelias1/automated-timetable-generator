from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.views.generic import ListView

from timetable.models import Class, Room

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
    
    
class ClassListView(ListView):
    model = Class
    paginate_by = 10
    
class ClassCreateView(CreateView):
    model = Class
    fields = ['name']
    
    def get_success_url(self):
        return reverse('classes')

class ClassDeleteView(DeleteView):
    model = Class
    success_url = reverse_lazy('classes')
    
class ClassUpdateView(UpdateView):
    model = Class
    fields = ['name']
    template_name_suffix = '_form'
    
    def get_success_url(self):
        return reverse('classes')