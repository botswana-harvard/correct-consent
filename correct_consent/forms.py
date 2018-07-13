from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

from .choices import MAP_AREAS


class MapAreaSelectionForm(forms.Form):

    map_area = forms.ChoiceField(
        choices=MAP_AREAS, label='Community Name')

    def __init__(self, *args, **kwargs):
        super(MapAreaSelectionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-2'
        self.helper.layout = Layout(
            'map_area',
            Submit('submit', u'Submit', css_class="btn btn-sm btn-default"),
        )


class SubjectIdentifierForm(forms.Form):

    subject_identifier = forms.CharField(label='Subject Identifier')

    def __init__(self, *args, **kwargs):
        super(SubjectIdentifierForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-2'
        self.helper.layout = Layout(
            'subject_identifier',
            Submit('submit', u'Submit', css_class="btn btn-sm btn-default"),
        )
