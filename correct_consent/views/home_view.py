from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from edc_base.view_mixins import EdcBaseViewMixin
from edc_consent.tests.models import SubjectConsent

from ..forms import SubjectIdentifierForm


class HomeView(EdcBaseViewMixin, TemplateView, FormView):

    form_class = SubjectIdentifierForm
    template_name = 'correct_consent/home.html'
    consent_model_wrapper_cls = None

    def consents(self, subject_identifier=None):
        """Return consents.
        """
        if subject_identifier:
            subject_consent = SubjectConsent.objects.filter(
                subject_identifier=subject_identifier)
        else:
            subject_consent = SubjectConsent.objects.all().order_by(
                '-modified')[:50]
        return subject_consent

    def form_valid(self, form):
        if form.is_valid():
            subject_identifier = form.cleaned_data['subject_identifier']
        context = self.get_context_data(**self.kwargs)
        context.update(
            form=form,
            consents=self.consents_wrapped(
                self.consents(subject_identifier=subject_identifier)))
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
        consents = None
        if not consents:
            consents = self.consents_wrapped(self.consents())
        context.update(
            consents=consents)
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
