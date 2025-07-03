from django import forms
from django.contrib.auth.forms import UserCreationForm

from mailing.forms import StyleFormMixin
from users.models import Profile, User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def clean_phone(self):
        phone_number = self.cleaned_data.get('phone')
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError('Номер телефона должен содержать только цифры')
        return phone_number


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'birth_date', 'profile_picture')
