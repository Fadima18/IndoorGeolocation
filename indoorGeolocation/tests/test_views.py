from django.test import TestCase, Client
from django.urls import reverse
from ..models import Device, Person, Material, Position


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.track_material_url = reverse("track_material")
        self.track_person_url = reverse("track_person")
        self.analytics_url = reverse("analytics")
        self.track_specific_material_url = 'http://localhost:8000/indoor/track_specific_material?name=Tv'
        self.track_specific_person_url = "http://localhost:8000/indoor/track_specific_person/noone?name=Mass"
        self.device = Device.objects.create(
            device_id="eui-193991",
            name="device1"
        )

    def testTrackMaterialShouldReturnTrackMaterialPage(self):
        reponse = self.client.get(self.track_material_url)

        self.assertEquals(reponse.status_code, 200)
        self.assertTemplateUsed("indoorGeolocation/material_tracking.html")

    def testTrackPersonShouldReturnTrackPersonPage(self):
        reponse = self.client.get(self.track_person_url)

        self.assertEquals(reponse.status_code, 200)
        self.assertTemplateUsed("indoorGeolocation/person_tracking.html")

    def testSpecificMaterialTrackingShouldReturnSpecificMaterialTrackingPage(self):
        Material.objects.create(
            device=self.device,
            name="Tv"
        )
        Position.objects.create(
            device=self.device,
            x=14.795036483073138,
            y=-16.9649700075388
        )
        reponse = self.client.get(self.track_specific_material_url)

        self.assertEquals(reponse.status_code, 200)
        self.assertTemplateUsed("indoorGeolocation/specific_object_tracking.html")

    def testAnalyticsShouldReturnAnalyticsPage(self):
        reponse = self.client.get(self.analytics_url)

        self.assertEquals(reponse.status_code, 200)
        self.assertTemplateUsed("indoorGeolocation/analytics.html")

    def testSpecificPersonTrackingShouldReturnSpecificPersonTrackingPage(self):
        Person.objects.create(
            device=self.device,
            firstName="Mass",
            lastName="Sene"
        )
        reponse = self.client.get(self.track_specific_person_url)

        self.assertEquals(reponse.status_code, 200)
        self.assertTemplateUsed("indoorGeolocation/specific_person_tracking.html")

    def testViewAnalyticsContext(self):
        reponse = self.client.get(self.analytics_url)
        context = reponse.context

        self.assertIsInstance(context['analytics'], bool)
        self.assertIsInstance(context['places'], bool)
        self.assertIsInstance(context['days_labels'], list)
        self.assertIsInstance(context['days_data'], list)
        self.assertIsInstance(context['today_visits'], int)

    def testPersonTrackingContext(self):
        reponse = self.client.get(self.track_person_url)
        context = reponse.context

        self.assertIsInstance(context['map'], str)
        self.assertIsInstance(context['person'], bool)

    def testMaterialTrackingContext(self):
        reponse = self.client.get(self.track_material_url)
        context = reponse.context

        self.assertIsInstance(context['map'], str)
        self.assertIsInstance(context['material'], bool)

    def testTrackSpecificPersonContext(self):
        reponse = self.client.get(self.track_material_url)
        context = reponse.context

        self.assertIsInstance(context['map'], str)
