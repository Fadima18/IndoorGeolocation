from django.test import TestCase, Client
from django.urls import reverse
from account.models import CustomAccount


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.login_url = reverse("login")
        self.register_url = reverse("registration")
        self.home_url = reverse("home")
        self.registration_template = "account/registration_index.html"
        self.login_template = "account/login.html"
        self.home_template="index.html"
        self.email = "email@email.com"

    def testHomeShouldReturnHomePage(self):
        reponse = self.client.get(self.home_url)

        self.assertEquals(reponse.status_code, 200)
        self.assertTemplateUsed(self.home_template)

    def testRegisterWithMethodNotPostShouldReturnRegistrationPage(self):
        reponse = self.client.get(self.register_url)

        self.assertEquals(reponse.status_code, 200)
        self.assertTemplateUsed(self.registration_template)

    def testRegisterWithValidPOSTDataShouldRedirect(self):
        reponse = self.client.post(self.register_url, {
            'firstName': "First",
            'lastName': "Last",
            'email': self.email,
            'password': "password1",
            'password2': "password1"
        }
        )
        accounts = CustomAccount.objects.all()

        self.assertEquals(reponse.status_code, 302)
        self.assertEquals(len(accounts), 1)
        self.assertFalse(accounts[0].id_in_org == "")

    def testRegisterPOSTWithNoDataShouldReturnRegistrationPage(self):
        reponse = self.client.post(self.register_url, {})
        accounts = CustomAccount.objects.all()

        self.assertEquals(reponse.status_code, 200)
        self.assertEquals(len(accounts), 0)
        self.assertTemplateUsed(self.registration_template)

    def testRegisterPOSTWithInvalidDataShouldReturnRegistrationPage(self):
        reponse = self.client.post(self.register_url, {
            'firstName': "First",
            'lastName': "Last",
            'email': self.email,
            'password': "password1",
            'password2': "password2"
        })
        accounts = CustomAccount.objects.all()

        self.assertEquals(reponse.status_code, 200)
        self.assertEquals(len(accounts), 0)
        self.assertTemplateUsed(self.registration_template)

    def testLoginWithMethodNotPostShouldReturnLoginPage(self):
        reponse = self.client.get(self.login_url)

        self.assertEquals(reponse.status_code, 200)
        self.assertTemplateUsed(self.login_template)

    def testLoginPOSTWithValidDataShouldRedirect(self):
        CustomAccount.objects.create(
            firstName="First",
            lastName="Last",
            email=self.email,
            password="password1",
            id_in_org="exampleid"
        )

        reponse = self.client.post(self.login_url, {
            'email': self.email,
            'id_in_org': "exampleid",
            'password': "password1"
        })

        self.assertEquals(reponse.status_code, 302)

    def testLoginPOSTWithNoDataShouldReturnLoginPage(self):
        reponse = self.client.post(self.login_url, {})

        self.assertEquals(reponse.status_code, 200)
        self.assertTemplateUsed(self.login_template)

    def testLoginPOSTWithInvalidDataShouldReturnLoginPage(self):
        reponse = self.client.post(self.login_url, {
            'email': self.email,
            'id_in_org': "exampleid",
            'password': "password1"
        })

        self.assertEquals(reponse.status_code, 200)
        self.assertTemplateUsed(self.login_template)
