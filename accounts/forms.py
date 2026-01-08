from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="Foydalanuvchi nomi",
        help_text="150 ta belgigacha. Harflar, raqamlar va @/./+/-/_ belgilariga ruxsat beriladi."
    )

    password1 = forms.CharField(
        label="Parol",
        widget=forms.PasswordInput,
        help_text="Parol kamida 8 ta belgidan iborat bo‘lishi kerak."
    )

    password2 = forms.CharField(
        label="Parolni tasdiqlash",
        widget=forms.PasswordInput,
        help_text="Tasdiqlash uchun yuqoridagi parolni qayta kiriting."
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Foydalanuvchi nomi",
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    password = forms.CharField(
        label="Parol",
        widget=forms.PasswordInput,
        strip=False
    )