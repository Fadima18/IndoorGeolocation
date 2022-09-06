from pyexpat import model
from django.db import models

# Create your models here.


class Device(models.Model):
    device_id = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class Position(models.Model):
    x = models.FloatField()
    y = models.FloatField()
    instant = models.DateTimeField(auto_now=True)
    device = models.ForeignKey(
        Device, related_name='device_positions', on_delete=models.CASCADE)
    def __str__(self):
        return self.device.name


class Node(models.Model):
    device = models.OneToOneField(
        Device, on_delete=models.PROTECT, blank=True, null=True)
    def __str__(self):
        return self.device.name


class Person(Node):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    def __str__(self):
        return self.firstName

class Material(Node):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
