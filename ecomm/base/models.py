# helper file common to many db

from django.db import models
import uuid

# models.Model is db's table but using meta makes sure that it is not considered as the db table
class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now =True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True