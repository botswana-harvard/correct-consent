from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from edc_base.view_mixins import EdcBaseViewMixin
from django.views.generic.edit import FormView

from bcpp_subject.models import SubjectConsent
from ..forms import MapAreaSelectionForm, SubjectIdentifierForm
from bcpp_subject_dashboard.model_wrappers import SubjectConsentModelWrapper


class HomeView(EdcBaseViewMixin, TemplateView, FormView):

    form_class = MapAreaSelectionForm
    template_name = 'correct_consent/home.html'
    consent_model_wrapper_cls = SubjectConsentModelWrapper

    def consents(self, map_area=None, subject_identifier=None):
        """Return consents.
        """
        if map_area:
            subject_consent = SubjectConsent.objects.filter(
                household_member__household_structure__household__plot__map_area=map_area)
        elif subject_identifier:
            subject_consent = SubjectConsent.objects.filter(
                subject_identifier=subject_identifier)
        else:
            subject_consent = SubjectConsent.objects.all().order_by(
                '-modified')[:50]
        return subject_consent

    def form_valid(self, form):
        if form.is_valid():
            map_area = form.cleaned_data['map_area']
        context = self.get_context_data(**self.kwargs)
        context.update(
            form=form,
            map_area=map_area,
            consents=self.consents_wrapped(self.consents(map_area=map_area)))
        return self.render_to_response(context)

    def consents_wrapped(self, consents=None):
        """Returns a list of wrapped consents.
        """
        if consents:
            return [
                self.consent_model_wrapper_cls(obj) for obj in consents]
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        map_area = 'all communities'
        subject_identifier_form = SubjectIdentifierForm()
        consents = None
        if self.request.method == 'POST':
            subject_identifier_form_instance = SubjectIdentifierForm(
                self.request.POST)
            if subject_identifier_form_instance.is_valid():
                subject_identifier = subject_identifier_form_instance.data[
                    'subject_identifier']
                consents = self.consents_wrapped(self.consents(
                    subject_identifier=subject_identifier))
        if not consents:
            consents = self.consents_wrapped(self.consents())
        context.update(
            consents=consents,
            map_area=map_area,
            subject_identifier_form=subject_identifier_form)
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
