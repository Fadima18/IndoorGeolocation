from django.test import SimpleTestCase
from ..utils import random_chars


class TestUtils(SimpleTestCase):

    def testRandomCharsShouldReturnString(self):
        id_org = random_chars(10)

        self.assertTrue(type(id_org) == str)
        self.assertEquals(len(id_org), 10)
