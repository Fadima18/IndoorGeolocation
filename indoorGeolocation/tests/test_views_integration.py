from django.test import TestCase
from django.urls import reverse
from django.test.client import Client
from ..models import Device, Person


class TestIntegration(TestCase):

    def test_track_person(self):
        c = Client()
        response = c.get(reverse("track_person"))
        context = response.context
        self.assertIsInstance(context['map'], str)
        self.assertIsInstance(context['person'], bool)
