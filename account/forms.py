from django import forms
from .models import CustomAccount


class RegistrationForm(forms.ModelForm):

    firstName = forms.CharField(
        label='First Name', max_length=50, help_text='Requis', required=True)
    lastName = forms.CharField(
        label='Last Name', max_length=50, help_text='Requis', required=True)
    email = forms.EmailField(
        max_length=100, label="Email", help_text='Requis', required=True)
    password = forms.CharField(
        label='Password', widget=forms.PasswordInput, help_text="Requis", required=True)
    password2 = forms.CharField(
        label='Password', widget=forms.PasswordInput, help_text="Requis", required=True)

    class Meta:
        model = CustomAccount
        exclude = ('id_in_org',)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError(
                'Les mots de passe ne sont pas les mêmes!')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomAccount.objects.filter(email=email).exists():
            raise forms.ValidationError('Cet addresse email existe déjà!')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['firstName'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Name'})
        self.fields['lastName'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Surname'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'email@email.com', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Confirm password'})


class LoginForm(forms.ModelForm):
    email = forms.EmailField(
        max_length=100, label="Email", help_text='Requis', required=True)
    id_in_org = forms.CharField(
        max_length=10, label="ID", help_text="requis", required=True)
    password = forms.CharField(
        label="Password", widget=forms.PasswordInput, help_text="Requis", required=True)

    class Meta:
        model = CustomAccount
        fields = ('email', 'id_in_org', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control input100 py-4', 'placeholder': 'Password'})
        self.fields['id_in_org'].widget.attrs.update(
            {'class': 'form-control mb-3 input100 py-4', 'placeholder': 'ID'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3 input100 py-4', 'placeholder': 'Email', 'name': 'email', 'id': 'id_email'})
