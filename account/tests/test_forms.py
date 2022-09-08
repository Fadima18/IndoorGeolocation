from django.test import TestCase
from account.forms import RegistrationForm, LoginForm
from account.models import CustomAccount


class TestForms(TestCase):

    def setUp(self):
        self.email = "email@email.com"
        self.login_data = {
            'email': self.email,
            'id_in_org': "xruaoot",
            'password': "password"
        }
        self.registration_data = {
            'firstName': "first",
            'lastName': "last",
            'email': self.email,
            'password': "password1",
            'password2': "password1"
        }

    def testLoginFormWithAllFieldsIsValid(self):
        form = LoginForm(data=self.login_data)

        self.assertTrue(form.is_valid())

    def testLoginFormWithIncorrectFieldTypeIsInvalid(self):
        form = LoginForm(data={
            'email': "email.com",
            'id_in_org': "xruaoot",
            'password': "password"
        })

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def testLoginFormWithMissingFieldsIsInvalid(self):
        form = LoginForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)

    def testRegistrationFormWithAllFieldsIsValid(self):
        form = RegistrationForm(data=self.registration_data)

        self.assertTrue(form.is_valid())

    def testRegistrationFormWithIncorrectFieldTypeIsInvalid(self):
        form = RegistrationForm(data={
            'firstName': "first",
            'lastName': "last",
            'email': "emailemailcom",
            'password': "password1",
            'password2': "password1"
        })

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def testRegistrationFormWithMissingFieldIsInvalid(self):
        form = RegistrationForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 5)

    def testRegistrationFormWithExistingEmailIsInvalid(self):
        CustomAccount.objects.create(
            firstName="First",
            lastName="Last",
            email=self.email,
            password="password1",
            id_in_org="xjzzjzj"
        )

        form = RegistrationForm(data={
            'firstName': "Second",
            'lastName': "Second",
            'email': self.email,
            'password': "password1",
            'password2': "password1"
        })

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def testRegistrationFormWithPasswordNotMatchingIsInvalid(self):
        form = RegistrationForm(data={
            'firstName': "first",
            'lastName': "last",
            'email': self.email,
            'password': "password1",
            'password2': "password2"
        })

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
