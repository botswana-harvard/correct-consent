from django.conf.urls import url

from .views import HomeView

app_name = 'correct_consent'

urlpatterns = [
    url(r'^', HomeView.as_view(), name='home_url'),
]