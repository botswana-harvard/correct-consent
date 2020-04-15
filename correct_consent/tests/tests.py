from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from model_mommy import mommy

from ..forms import CorrectConsentForm
from ..models import SubjectConsent


@tag('cc')
class TestCorrectConsent(TestCase):

    def setUp(self):
        self.subject_consent = mommy.make_recipe(
            'correct_consent.subjectconsent')

        self.options = {
            'old_identity': self.subject_consent.identity,
            'new_identity': '44425678',
            'report_datetime': get_utcnow(),
            'subject_consent': self.subject_consent,
            'new_first_name': None,
            'old_first_name': None,
            'new_last_name': None,
            'old_last_name': None
        }

    def test_form_is_ok(self):
        correct_consent_form = CorrectConsentForm(cleaned_data=self.options)
        self.assertIsInstance(self.subject_consent, SubjectConsent)
        try:
            correct_consent_form.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_identity_match_invalid(self):
        self.options['old_identity'] = '44424444'
        correct_consent_form = CorrectConsentForm(cleaned_data=self.options)
        self.assertRaises(ValidationError, correct_consent_form.validate)
        self.assertIn('old_identity', correct_consent_form._errors)

    def test_old_initials_match_invalid(self):
        self.options['old_initials'] = 'TT'
        correct_consent_form = CorrectConsentForm(cleaned_data=self.options)
        self.assertRaises(ValidationError, correct_consent_form.validate)
        self.assertIn('old_initials', correct_consent_form._errors)

    def test_initials_match_valid(self):
        self.options['old_initials'] = self.subject_consent.initials
        correct_consent_form = CorrectConsentForm(cleaned_data=self.options)
        try:
            correct_consent_form.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_no_old_identity_new_invalid(self):
        self.options['old_identity'] = None
        correct_consent_form = CorrectConsentForm(cleaned_data=self.options)
        self.assertRaises(ValidationError, correct_consent_form.validate)
        self.assertIn('old_identity', correct_consent_form._errors)

    def test_no_old_first_name_new_invalid(self):
        self.options['old_first_name'] = None
        self.options['new_first_name'] = self.subject_consent.first_name
        correct_consent_form = CorrectConsentForm(cleaned_data=self.options)
        self.assertRaises(ValidationError, correct_consent_form.validate)
        self.assertIn('old_first_name', correct_consent_form._errors)

#     def test_old_initials_match_invalid(self):
#         self.options['old_initials'] = self.subject_consent.initials
#         self.options['old_initials'] = 'TT'
#         correct_consent_form = CorrectConsentForm(data=self.options)
#         self.assertFalse(correct_consent_form.is_valid())
#         self.assertIn('old_initials', correct_consent_form.errors)

#         self.assertIsInstance(self.subject_consent, SubjectConsent)
#         self.assertTrue(correct_consent_form.is_valid())
#         self.assertTrue(correct_consent_form.save()) form.errors
