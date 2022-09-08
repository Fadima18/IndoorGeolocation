from django.shortcuts import render, redirect
from account.models import CustomAccount
from .forms import RegistrationForm, LoginForm
from .utils import random_chars
# Create your views here.


def view_home(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        registerform = RegistrationForm(request.POST)
        if registerform.is_valid():
            user = CustomAccount()
            user.firstName = registerform.cleaned_data['firstName']
            user.lastName = registerform.cleaned_data['lastName']
            user.email = registerform.cleaned_data['email']
            user.password = registerform.cleaned_data['password']
            id_in_org = random_chars(10)
            user.id_in_org = id_in_org
            user.save()
            return redirect('analytics')
    else:
        registerform = RegistrationForm()
    return render(request, 'registration_index.html', {'form': registerform})


def login(request):
    if request.method == 'POST':
        loginform = LoginForm(request.POST)
        email = loginform["email"].value()
        password = loginform["password"].value()
        id_in_org = loginform["id_in_org"].value()
        if CustomAccount.objects.filter(email=email).exists():
            user = CustomAccount.objects.filter(email=email)[0]
            if user.password == password and user.id_in_org == id_in_org:
                return redirect('analytics')
    else:
        loginform = LoginForm()
    return render(request, 'login.html', {'form': loginform})
