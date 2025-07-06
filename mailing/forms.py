from django import forms
from django.forms import BooleanField, ModelForm

from mailing.models import Mailing, Recipient, Message


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs['class'] = 'form-check-input'
            else:
                fild.widget.attrs['class'] = 'form-control'


class MailingForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['recipient'].queryset = Recipient.objects.filter(user=user)
        self.fields['message'].queryset = Message.objects.filter(user=user)


    class Meta:
        model = Mailing
        fields = ['message', 'recipient', 'status']


