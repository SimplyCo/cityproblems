from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'cityproblems.site.views.home', name='home'),
)
