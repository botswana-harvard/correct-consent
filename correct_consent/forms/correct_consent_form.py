from django import forms
from edc_form_validators import FormValidator
from ..models import CorrectConsent


class CorrectConsentForm(FormValidator, forms.ModelForm):

    def clean(self):
#         cleaned_data = super().clean()

        self.subject_consent = self.cleaned_data.get('subject_consent')

        self.validate_identity(subject_consent=self.subject_consent)
        self.validate_initials()

        fields = ['identity', 'first_name', 'last_name', 'dob', 'gender',
                  'guardian_nam', 'may_store_samples', 'is_literate',
                  'witness_name']

        for f in fields:
            self.required_if_not_none(
                field='new' + f,
                field_required='old' + f)

    def validate_identity(self, subject_consent=None):
        old_identity = self.cleaned_data.get('old_identity')
        if (old_identity
                and subject_consent.identity != old_identity):

            raise forms.ValidationError(
                {'old_identity': f'The old_identity does not match the '
                 f'identity from the subject\'s consent. Got {old_identity}, '
                 f'expected {subject_consent.identity}.'})

    def validate_initials(self):

        subject_consent = self.cleaned_data.get('subject_consent')

        first_name = self.cleaned_data.get('new_first_name') or subject_consent.first_name

        last_name = self.cleaned_data.get('new_last_name') or subject_consent.last_name

        new_initials = self.cleaned_data.get('new_initials')

        old_initials = self.cleaned_data.get('old_initials')
        if old_initials:

            if subject_consent.initials != old_initials:

                raise forms.ValidationError(
                    {'old_initials': f'The old_intials does not match the '
                     f'initials from the subject\'s consent. Got {old_initials}, '
                     f'expected {subject_consent.initials}.'})

            if (new_initials and not (new_initials.startswith(first_name[0])
                                      and new_initials.endswith(last_name[0]))):
                raise forms.ValidationError(
                    {'new_initials': 'New initials do not match first and '
                     'last name. Expected initials that start with '
                     f'{first_name[0]} and end with {last_name[0]}, '
                     f'Got {self.new_initials}'})

#     def validate_new_name(self):

#     def validate_old_field(self, consent=None, old_field=None):
#
#         if consent and old_field:
#             consent_field = old_field[4:]
#             if consent

    class Meta:
        model = CorrectConsent
        fields = '__all__'
