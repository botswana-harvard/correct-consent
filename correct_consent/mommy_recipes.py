from dateutil.relativedelta import relativedelta
from django.contrib.sites.models import Site
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO
from faker import Faker
from model_mommy.recipe import Recipe, seq

from .models import SubjectConsent, CorrectConsent

fake = Faker()

subjectconsent = Recipe(
    SubjectConsent,
    report_datetime=get_utcnow(),
    identity=seq('12325678', increment_by=1),
    confirm_identity=seq('12325678', increment_by=1),
    first_name=fake.first_name,
    last_name=fake.last_name,
    initials='XX',
    dob=get_utcnow() - relativedelta(years=25),
    gender='F',
    is_literate=YES,
    is_incarcerated=NO,
    assessment_score=YES,
    consent_copy=YES,
    consent_datetime=get_utcnow(),
    consent_reviewed=YES,
    is_dob_estimated='-',
    study_questions=YES,
    site=Site.objects.get_current(),
    subject_identifier=None)
