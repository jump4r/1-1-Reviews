from django.conf.urls import url
from webapp.views import AppView

urlpatterns = [url(r'^$', AppView.as_view())]