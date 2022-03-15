from django.urls import path
from timetable.views import SubjectCreateView, SubjectDeleteView, SubjectListView, SubjectUpdateView, InstructorCreateView, InstructorDeleteView, InstructorListView, InstructorUpdateView, RoomCreateView, RoomDeleteView, RoomListView, RoomUpdateView, SectionCreateView, SectionDeleteView, SectionListView, SectionUpdateView, index, settings


urlpatterns = [
    path('', index),
    path('rooms/', RoomListView.as_view(), name='rooms'),
    path('rooms/create/', RoomCreateView.as_view(), name='create_room'),
    path('rooms/delete/<uuid:pk>/', RoomDeleteView.as_view(), name='delete-room'),
    path('rooms/edit/<uuid:pk>/', RoomUpdateView.as_view(), name='edit-room'),

    path('subjects/', SubjectListView.as_view(), name='subjects'),
    path('subjects/create/', SubjectCreateView.as_view(), name='create-subject'),
    path('subjects/delete/<uuid:pk>/',
         SubjectDeleteView.as_view(), name='delete-subject'),
    path('subjects/edit/<uuid:pk>/', SubjectUpdateView.as_view(), name='edit-subject'),

    path('sections/', SectionListView.as_view(), name='sections'),
    path('sections/create/', SectionCreateView.as_view(), name='create-section'),
    path('sections/delete/<uuid:pk>/',
         SectionDeleteView.as_view(), name='delete-section'),
    path('sections/edit/<uuid:pk>/', SectionUpdateView.as_view(), name='edit-section'),
    
    path('instructors/', InstructorListView.as_view(), name='instructors'),
    path('instructors/create/', InstructorCreateView.as_view(), name='create-instructor'),
    path('instructors/delete/<uuid:pk>/',
         InstructorDeleteView.as_view(), name='delete-instructor'),
    path('instructors/edit/<uuid:pk>/', InstructorUpdateView.as_view(), name='edit-instructor'),
    
    path('settings/', settings, name='settings'),
]
