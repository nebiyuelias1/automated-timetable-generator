from django.urls import path
from timetable.views import classes, index, instructors, rooms, sections, settings


urlpatterns = [
    path('', index),
    path('rooms/', rooms, name='rooms'),
    path('classes/', classes, name='classes'),
    path('sections/', sections, name='sections'),
    path('instructors/', instructors, name='instructors'),
    path('settings/', settings, name='settings'),
]
