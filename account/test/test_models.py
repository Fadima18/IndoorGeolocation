from django.test import TestCase
from account.models import CustomAccount
import string
import random


class TestModels(TestCase):

    def setUp(self):
        self.account = CustomAccount.objects.create(
            firstName="First",
            lastName="Last",
            email="email@email.com",
            password="password1",
            id_in_org="xyaolapr"
        )

    def testAccountIsCreated(self):
        accounts = CustomAccount.objects.all()
        self.assertEquals(accounts[0], self.account)
        self.assertEquals(accounts[0].firstName, "First")
        self.assertEquals(accounts[0].lastName, "Last")
        self.assertEquals(accounts[0].email, "email@email.com")
        self.assertEquals(accounts[0].password, "password1")
        self.assertEquals(accounts[0].id_in_org, "xyaolapr")

    def testStrIsCalled(self):
        self.assertEquals(str(self.account), "First Last")
