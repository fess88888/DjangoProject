from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Почта", widget=forms.EmailInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    phone = forms.CharField(label="Номер телефона", required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    country = forms.CharField(label="Страна", required=False, widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ["email", "phone", "country", "avatar"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not field.widget.attrs.get("class"):
                field.widget.attrs["class"] = "form-control"

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с такой почтой уже зарегистрирован.")
        return email


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Почта", widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-control"}))
