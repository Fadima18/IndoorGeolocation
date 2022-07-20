from pyexpat import model
from django.db import models

# Create your models here.

class Device(models.Model):
    device_id = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    
class Position(models.Model):
    x = models.FloatField()
    y = models.FloatField()
    instant = models.DateTimeField(auto_now=True)
    device = models.ForeignKey(Device, related_name='device_positions', on_delete=models.CASCADE)
    
