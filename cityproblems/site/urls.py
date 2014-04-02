from django.conf.urls import patterns, include, url

urlpatterns = patterns('cityproblems.site.views',
                       url(r'^cabinet/$', 'user_cabinet', name='site_user_cabinet'),
                       url(r'^$', 'home', name='home'),
                       url(r'^denied/$', 'no_permissions', name='no_permissions'),
                       url(r'^create_problem/$', 'create_problem', name='site_create_problem'),
                       url(r'^edit/problem/(\d+)/$', 'edit_problem', name='site_edit_problem'),
                       url(r'^add/problem/(\d+)/$', 'edit_problem', name='site_add_problem'),
                       )

