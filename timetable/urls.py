from django.urls import path
from timetable.views import index


urlpatterns = [
    path('', index)
]
