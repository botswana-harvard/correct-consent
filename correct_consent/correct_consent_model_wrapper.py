from django.apps import apps as django_apps
from edc_model_wrapper import ModelWrapper


class CorrectConsentModelWrapper(ModelWrapper):

    model = 'bcpp_subject.correctconsent'
    next_url_name = django_apps.get_app_config(
        'bcpp_subject_dashboard').dashboard_url_name
    next_url_attrs = ['subject_identifier', 'survey_schedule']
    querystring_attrs = ['subject_consent']

    @property
    def subject_consent(self):
        return str(self.object.subject_consent.id)

    @property
    def survey_schedule(self):
        return self.object.subject_consent.survey_schedule