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

class Node(models.Model):
    device = models.OneToOneField(Device, on_delete=models.PROTECT)

class Person(Node):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    
class Material(Node):
    name = models.CharField(max_length=50)