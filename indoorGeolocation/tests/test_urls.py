from django.test import TestCase
from django.urls import resolve, reverse
from ..views import track_material, track_person, track_specific_material, track_specific_person, view_analytics
from ..models import Device, Person

class TestUrls(TestCase):

    def setUp(self):
        self.device = Device.objects.create(
            device_id = "eui-193991",
            name = "device1"
        )
    
    def testTrackMaterialUrlResolve(self):
        url = reverse("track_material")
        self.assertEquals(resolve(url).func, track_material)
        
    def testTrackSpecififMaterialResolve(self):
        url = reverse("track_specific_material")
        self.assertEquals(resolve(url).func, track_specific_material)
        
    def testAnalyticsResolve(self):
        url = reverse("analytics")
        self.assertEquals(resolve(url).func, view_analytics)
        
    def testTrackPerson(self):
        url = reverse("track_person")
        self.assertEquals(resolve(url).func, track_person)
        
    def testTrackSpecificPerson(self):
        Person.objects.create(
            device = self.device,
            firstName = "Moussa",
            lastName = "Niang"
        )
        url = reverse("track_specific_person", args=["Moussa"])
        self.assertEquals(resolve(url).func, track_specific_person)
        