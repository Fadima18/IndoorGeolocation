from django.db import models
from indoorGeolocation.models import Person

# Create your models here.


class CustomAccount(Person):

    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=25)
    id_in_org = models.CharField(max_length=10, unique=True)

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def __str__(self):
        return self.firstName + " " + self.lastName
