from django import forms
from django.forms import BooleanField, ModelForm

from mailing.models import Mailing, Recipient


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs['class'] = 'form-check-input'
            else:
                fild.widget.attrs['class'] = 'form-control'


class MailingForm(StyleFormMixin, ModelForm):
    recipients = forms.ModelMultipleChoiceField(
        queryset=Recipient.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Получатели"
    )

    class Meta:
        model = Mailing
        fields = ['message', 'recipients', 'status']
