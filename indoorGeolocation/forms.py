from secrets import choice
from django import forms

class RoomForm(forms.Form):
    CHOICES = (("Chambre10", "Chambre 10"), ("Chambre9", "Chambre 9"), ("Chambre8", "Chambre 8"), ("Chambre7", "Chambre 7"), ("Chambre6", "Chambre 6"), ("Chambre5", "Chambre 5"))
    room = forms.ChoiceField(choices=CHOICES)