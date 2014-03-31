from django.conf.urls import patterns, include, url

urlpatterns = patterns('cityproblems.site.views',
                       url(r'^user_cabinet/$', 'user_cabinet', name='site_user_cabinet'),
                       url(r'^$', 'home', name='home'),
                       url(r'^$', 'no_permissions', name='no_permissions'),
                       )

