from distutils.log import Log
from django.shortcuts import render, redirect
from account.models import CustomAccount
from .forms import RegistrationForm, LoginForm
import string
import random

# Create your views here.


def register(request):
    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = CustomAccount()
            user.firstName = registerForm.cleaned_data['firstName']
            user.lastName = registerForm.cleaned_data['lastName']
            user.email = registerForm.cleaned_data['email']
            user.password = registerForm.cleaned_data['password']
            letters = string.ascii_lowercase
            id = ''.join(random.choice(letters) for i in range(10))
            user.id_in_org = id
            user.save()
            return redirect('analytics')
    else:
        registerForm = RegistrationForm()
    return render(request, 'registration_index.html', {'form': registerForm})


def login(request):
    if request.method == 'POST':
        loginForm = LoginForm(request.POST)
        email = loginForm["email"].value()
        password = loginForm["password"].value()
        id_in_org = loginForm["id_in_org"].value()
        if CustomAccount.objects.filter(email=email).exists():
            user = CustomAccount.objects.filter(email=email)[0]
            if user.password == password and user.id_in_org == id_in_org:
                return redirect('analytics')
    else:
        loginForm = LoginForm()
    return render(request, 'login.html', {'form': loginForm})
