from multiprocessing import context
from unittest import TestCase
from multiprocessing import context
from urllib import response
from django.urls import reverse
from django.test.client import Client


class TestIntegration(TestCase):
    def test_track_person(self):
        c = Client()
        response = c.get(reverse("track_person"))
        context= response.context
        self.assertIsInstance(context['map'], str)
        self.assertIsInstance(context['person'], bool)

