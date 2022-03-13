from django.urls import path
from timetable.views import ClassCreateView, ClassDeleteView, ClassListView, ClassUpdateView, RoomCreateView, RoomDeleteView, RoomListView, RoomUpdateView, SectionCreateView, SectionDeleteView, SectionListView, SectionUpdateView, index, instructors, sections, settings


urlpatterns = [
    path('', index),
    path('rooms/', RoomListView.as_view(), name='rooms'),
    path('rooms/create/', RoomCreateView.as_view(), name='create_room'),
    path('rooms/delete/<uuid:pk>/', RoomDeleteView.as_view(), name='delete-room'),
    path('rooms/edit/<uuid:pk>/', RoomUpdateView.as_view(), name='edit-room'),

    path('classes/', ClassListView.as_view(), name='classes'),
    path('classes/create/', ClassCreateView.as_view(), name='create-class'),
    path('classes/delete/<uuid:pk>/',
         ClassDeleteView.as_view(), name='delete-class'),
    path('classes/edit/<uuid:pk>/', ClassUpdateView.as_view(), name='edit-class'),

    path('sections/', SectionListView.as_view(), name='sections'),
    path('sections/create/', SectionCreateView.as_view(), name='create-section'),
    path('sections/delete/<uuid:pk>/',
         SectionDeleteView.as_view(), name='delete-section'),
    path('sections/edit/<uuid:pk>/', SectionUpdateView.as_view(), name='edit-section'),
    
    path('instructors/', instructors, name='instructors'),
    path('settings/', settings, name='settings'),
]
