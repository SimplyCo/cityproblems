from django.conf.urls import patterns, include, url

from .views import UserDashboard

urlpatterns = patterns('cityproblems.site.views',
                       url(r'^$', 'home', name='home'),
                       url(r'^denied/$', 'no_permissions', name='no_permissions'),
                       url(r'^create_problem/$', 'create_problem', name='site_create_problem'),
                       url(r'^edit/problem/(\d+)/$', 'edit_problem', name='site_edit_problem'),
                       url(r'^add/problem/(\d+)/$', 'edit_problem', name='site_add_problem'),
                       url(r'^problem/$', 'problem_view', name='site_problem_view'),
                       url(r'^problem/(\d+)/$', 'problem_view', name='site_problem_view'),
                       url(r'^process_follow/$', 'process_follow', name='site_process_follow'),
                       url(r'^process_problem_status_change/(\d+)/$', 'process_problem_status_change', name='site_process_problem_status_change'),
                       url(r'^get_main_page_markers/$', 'get_main_page_markers', name='site_get_main_page_markers'),
                       )

urlpatterns += patterns('',
                        url(r'^dashboard/$', UserDashboard.as_view(), {"reportBy": "me", "status": "all", "category": "all"}, name='site_user_dashboard'),
                        url(r'^dashboard/(?P<reportBy>\w+)/(?P<status>\w+)/(?P<category>\w+)/$', UserDashboard.as_view(), name='site_user_dashboard'),
                        )
