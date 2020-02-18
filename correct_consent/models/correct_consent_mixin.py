from django.core.exceptions import ValidationError
from edc_base.utils import age


class CorrectConsentMixin:

    def update_initials(self, required_models=None,
                        first_name=None,
                        last_name=None):

        initials = first_name[0] + last_name[0]

        for model in required_models:
            if self.new_initials:
                if (self.new_initials.startswith(first_name[0]) and
                        self.new_initials.endswith(last_name[0])):
                    model.initials = self.new_initials
                    model.save(update_fields=['new_initials', 'user_modified'])
                else:
                    raise ValidationError(
                        'New initials do not match first and '
                        f'last name. Expected {initials}, '
                        f'Got {self.new_initials}')
        return initials

    def update_gender(self, required_models=None):
        for model in required_models:
            if self.new_gender:
                model.gender = self.new_gender
                model.save(update_fields=['new_gender', 'user_modified'])

    def update_dob(self, required_models=None, age_models=None):

        for model in required_models:
            if self.new_dob:
                model.dob = self.new_dob
                model.save()
                # Update Age in Years
                for age_model in age_models:
                    age_model.age = age(self.new_dob,
                                        age_model.report_datetime)
                    age_model.save(
                        update_fields=['age_in_years', 'user_modified'])

    class Meta:
        abstract = True
