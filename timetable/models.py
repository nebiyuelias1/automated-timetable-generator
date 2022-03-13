import uuid
from django.db import models

# Create your models here.
class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=500)
    
    def __str__(self) -> str:
        return self.name
