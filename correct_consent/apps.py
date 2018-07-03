from django.apps import AppConfig as DjangoApponfig


class AppConfig(DjangoApponfig):
    name = 'correct_consent'

    base_template_name = 'edc_base/base.html'

    listboard_template_name = 'correct_consent/listboard.html'
    listboard_url_name = 'correct_consent:listboard_url'
