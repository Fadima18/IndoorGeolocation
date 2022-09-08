from django.test import SimpleTestCase
from django.urls import resolve, reverse
from account.views import login, register, view_home


class TestUrls(SimpleTestCase):

    def testRegistrationUrlResolves(self):
        url = reverse("registration")
        self.assertEquals(resolve(url).func, register)

    def testLoginUrlResolves(self):
        url = reverse("login")
        self.assertEquals(resolve(url).func, login)

    def testHomeUrlResolves(self):
        home_url = reverse("home")
        self.assertEquals(resolve(home_url).func, view_home)
