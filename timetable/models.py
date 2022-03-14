import uuid
from django.db import models

class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=500)
    
    def __str__(self) -> str:
        return self.name

class Instructor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=500)
    
    def __str__(self) -> str:
        return self.name
    
class Subject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=500)
    
    instructors = models.ManyToManyField(Instructor, related_name='subjects')
    
    def __str__(self) -> str:
        return self.name
    
class Section(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=500)
    
    def __str__(self) -> str:
        return self.name
    


