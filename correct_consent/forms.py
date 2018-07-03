from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

from .choices import MAP_AREAS


class MapAreaSelectionForm(forms.Form):

    map_area = forms.ChoiceField(
        choices=MAP_AREAS, required=True, label='Community Name')

    def __init__(self, *args, **kwargs):
        super(MapAreaSelectionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-2'
        self.helper.layout = Layout(
            'map_area',  # field1 will appear first in HTML
            Submit('submit', u'Submit', css_class="btn btn-sm btn-default"),
        )