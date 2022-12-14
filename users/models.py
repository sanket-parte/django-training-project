from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, blank=True, null=True)
    username = models.CharField(max_length=256, blank=True, null=True)
    short_intro = models.CharField(max_length=256, blank=True, null=True)
    bio = models.TextField(max_length=1000,blank=True,null=True)
    
    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'profile'