from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    # ex: /testview/5/
    url(r'^testrun/(?P<testrun_id>[0-9]+)/$', views.testrun, name='testrun'),
    # ex: /testview/5/results/
    url(r'^testrun/(?P<testrun_id>[0-9]+)/testsuite/(?P<testsuite_id>[0-9]+)/$', views.testsuite, name='testsuite'),
    # ex: /testview/5/item/3
    url(r'^testrun/(?P<testitem_id>[0-9]+)//$', views.testitem, name='testitem'),
]
