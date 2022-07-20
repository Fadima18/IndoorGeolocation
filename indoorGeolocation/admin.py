from django.contrib import admin
from .models import Device, Position

# Register your models here.

admin.site.register([Device, Position])