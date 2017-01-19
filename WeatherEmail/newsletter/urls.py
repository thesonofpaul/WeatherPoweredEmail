from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^submit/$', views.submit, name='submit'),
    url(r'^(?P<pk>[0-9]+)/result/$', views.ResultView.as_view(), name='result')
]
