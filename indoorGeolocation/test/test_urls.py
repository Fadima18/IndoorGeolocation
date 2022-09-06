from django.test import SimpleTestCase
from django.urls import resolve, reverse
from ..views import *

class TestUrls(SimpleTestCase):
    
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
        url = reverse("track_specific_person", args=["Massamba"])
        self.assertEquals(resolve(url).func, track_specific_person)
        