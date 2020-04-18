from django import forms
from users.models import User


class RegisterForm(forms.Form):
    username = forms.CharField(required=True, min_length=4, max_length=20,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'username_id'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control',
                                                           'id': 'email_id',
                                                           'placeholder': 'example@example.com'}))
    password = forms.CharField(required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'id': 'password_id'}))
    password2 = forms.CharField(required=True,
                                label="Repeat password",
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password2') != cleaned_data.get('password'):
            self.add_error('password2', 'Passwords do not match')

    def save(self):
        return User.objects.create_user(
                self.cleaned_data.get('username'),
                self.cleaned_data.get('email'),
                self.cleaned_data.get('password')
            )
