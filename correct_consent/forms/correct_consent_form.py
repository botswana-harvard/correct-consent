from django import forms
from ..models import CorrectConsent


class CorrectConsentForm(forms.ModelForm):

    class Meta:
        model = CorrectConsent
        fields = '__all__'
