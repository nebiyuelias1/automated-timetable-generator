from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'timetable/index.html')

def rooms(request):
    return render(request, 'timetable/rooms.html')

def sections(request):
    return render(request, 'timetable/sections.html')

def classes(request):
    return render(request, 'timetable/classes.html')

def instructors(request):
    return render(request, 'timetable/instructors.html')

def settings(request):
    return render(request, 'timetable/settings.html')
