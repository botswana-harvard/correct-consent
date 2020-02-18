
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.deletion import PROTECT
from django_crypto_fields.fields import (FirstnameField, EncryptedCharField,
                                         LastnameField, IdentityField)
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import datetime_not_future
from edc_consent.tests.models import SubjectConsent
from edc_constants.choices import GENDER_UNDETERMINED, YES_NO

from .correct_consent_mixin import CorrectConsentMixin


class CorrectConsent(CorrectConsentMixin, BaseUuidModel):

    """A model linked to the subject consent to record corrections."""

    subject_consent = models.OneToOneField(
        SubjectConsent, on_delete=PROTECT)

    report_datetime = models.DateTimeField(
        verbose_name="Correction report date ad time",
        null=True,
        validators=[
            datetime_not_future],
    )

    old_identity = IdentityField(
        null=True,
        blank=True)

    new_identity = IdentityField(
        null=True,
        blank=True)

    old_first_name = FirstnameField(
        null=True,
        blank=True,
    )

    new_first_name = FirstnameField(
        null=True,
        blank=True,
    )

    old_last_name = LastnameField(
        null=True,
        blank=True,
    )
    new_last_name = LastnameField(
        null=True,
        blank=True,
    )

    old_initials = EncryptedCharField(
        blank=True,
        null=True,
        validators=[RegexValidator(
            regex=r'^[A-Z]{2,3}$',
            message=('Ensure initials consist of letters only in upper case'
                     ', no spaces.')), ],
    )

    new_initials = EncryptedCharField(
        validators=[RegexValidator(
            regex=r'^[A-Z]{2,3}$',
            message=('Ensure initials consist of letters only in upper case, '
                     'no spaces.')), ],
        null=True,
        blank=True,
    )

    old_dob = models.DateField(
        verbose_name="Old Date of birth",
        null=True,
        blank=True,
        help_text="Format is YYYY-MM-DD",
    )

    new_dob = models.DateField(
        verbose_name="New Date of birth",
        null=True,
        blank=True,
        help_text="Format is YYYY-MM-DD",
    )

    old_gender = models.CharField(
        choices=GENDER_UNDETERMINED,
        blank=True,
        null=True,
        max_length=1)

    new_gender = models.CharField(
        choices=GENDER_UNDETERMINED,
        max_length=1,
        null=True,
        blank=True,
    )

    old_guardian_name = LastnameField(
        validators=[
            RegexValidator('^[A-Z]{1,50}\, [A-Z]{1,50}$',
                           'Invalid format. Format is '
                           '\'LASTNAME, FIRSTNAME\'. All uppercase '
                           'separated by a comma')],
        blank=True,
        null=True,
    )

    new_guardian_name = LastnameField(
        validators=[
            RegexValidator('^[A-Z]{1,50}\, [A-Z]{1,50}$',
                           'Invalid format. Format is \'LASTNAME, '
                           'FIRSTNAME\'.  All uppercase separated '
                           'by a comma')],
        blank=True,
        null=True,
    )

    old_may_store_samples = models.CharField(
        verbose_name="Old Sample storage",
        max_length=3,
        blank=True,
        null=True,
        choices=YES_NO,
    )

    new_may_store_samples = models.CharField(
        verbose_name="New Sample storage",
        max_length=3,
        blank=True,
        null=True,
        choices=YES_NO,
    )

    old_is_literate = models.CharField(
        verbose_name="(Old) Is the participant LITERATE?",
        max_length=3,
        blank=True,
        null=True,
        choices=YES_NO,
    )

    new_is_literate = models.CharField(
        verbose_name="(New) Is the participant LITERATE?",
        max_length=3,
        blank=True,
        null=True,
        choices=YES_NO,
    )

    old_witness_name = LastnameField(
        verbose_name="Old Witness\'s Last and first name (illiterates only)",
        validators=[
            RegexValidator(
                '^[A-Z]{1,50}\, [A-Z]{1,50}$',
                'Invalid format. Format '
                'is \'LASTNAME, FIRSTNAME\'. All '
                'uppercase separated by a comma')],
        blank=True,
        null=True,
        help_text=('Required only if subject is illiterate. '
                   'Format is \'LASTNAME, FIRSTNAME\'. '
                   'All uppercase separated by a comma'),
    )

    new_witness_name = LastnameField(
        verbose_name="New Witness\'s Last and first name (illiterates only)",
        validators=[
            RegexValidator(
                '^[A-Z]{1,50}\, [A-Z]{1,50}$',
                'Invalid format. Format is \'LASTNAME, FIRSTNAME\'. '
                'All uppercase separated by a comma')],
        blank=True,
        null=True,
        help_text=('Required only if subject is illiterate. '
                   'Format is \'LASTNAME, FIRSTNAME\'. '
                   'All uppercase separated by a comma'),
    )

#     objects = CorrectConsentManager()

    history = HistoricalRecords()

    def natural_key(self):
        return self.subject_consent.natural_key()

    class Meta:
        app_label = 'correct_consent'
