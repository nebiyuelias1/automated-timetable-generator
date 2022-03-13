from django.forms import ModelForm

from timetable.models import Room

class RoomForm(ModelForm):
    class Meta:
        model = Room