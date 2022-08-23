from django.contrib import admin
from .models import Device, Position, Person, Material

# Register your models here.

admin.site.register([Device, Position, Person, Material])