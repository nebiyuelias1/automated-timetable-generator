from django.urls import path
from timetable.views import RoomCreateView, RoomDeleteView, RoomListView, RoomUpdateView, classes, index, instructors, sections, settings


urlpatterns = [
    path('', index),
    path('rooms/', RoomListView.as_view(), name='rooms'),
    path('rooms/create/', RoomCreateView.as_view(), name='create_room'),
    path('rooms/delete/<uuid:pk>/', RoomDeleteView.as_view(), name='delete-room'),
    path('rooms/edit/<uuid:pk>/', RoomUpdateView.as_view(), name='edit-room'),
    path('classes/', classes, name='classes'),
    path('sections/', sections, name='sections'),
    path('instructors/', instructors, name='instructors'),
    path('settings/', settings, name='settings'),
]
