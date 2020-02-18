from django.test import TestCase
from edc_base.utils import get_utcnow
from model_mommy import mommy

from ..forms import CorrectConsentForm
from ..models import SubjectConsent


class TestCorrectConsent(TestCase):

    def setUp(self):
        self.subject_consent = mommy.make_recipe(
            'correct_consent.subjectconsent')

        self.options = {
            'old_identity': self.subject_consent.identity,
            'new_identity': '44425678',
            'report_datetime': get_utcnow(),
            'subject_consent': self.subject_consent
        }

#         correct_consent = CorrectConsent.objects.create(
#             old_identity=self.subject_consent,
#             new_identity='44425678')

    def test_form_is_ok(self):
        correct_consent_form = CorrectConsentForm(data=self.options)
        self.assertIsInstance(self.subject_consent, SubjectConsent)
        self.assertTrue(correct_consent_form.is_valid())
        self.assertTrue(correct_consent_form.save())

    def test_identity_match(self):
        self.options['old_identity'] = '44424444'
        correct_consent_form = CorrectConsentForm(data=self.options)
        self.assertIsInstance(self.subject_consent, SubjectConsent)
        self.assertTrue(correct_consent_form.is_valid())
        self.assertTrue(correct_consent_form.save())
