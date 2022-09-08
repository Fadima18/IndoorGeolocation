from django.test import TestCase
from secrets import choice
from indoorGeolocation.forms import RoomForm


class TestForm(TestCase):
    def test_form(self):
        form_data = {"room": "Chambre9"}
        form = RoomForm(data=form_data)
        self.assertTrue(form.is_valid())
