import sys

from django.conf import settings
from .correct_consent import CorrectConsent

if settings.APP_NAME == 'correct_consent' or test in sys.argv:
    from edc_consent.tests.models import SubjectConsent
