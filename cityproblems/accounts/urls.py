from django.conf.urls import patterns, url


urlpatterns = patterns('cityproblems.accounts.views',
                       url(r'^register/$', 'register', name="accounts_register"),
                       url(r'^profile/edit/$', 'accounts_profile_edit', name="accounts_profile_edit"),
                       url(r'^profile/$', 'accounts_profile_view', name="accounts_profile_view"),
                       url(r'^profile/(\w+)/$', 'accounts_profile_view', name="accounts_profile_view"),
                       url(r'^send_email_confirm_link/$', 'accounts_send_email_confirm_link', name="accounts_send_email_confirm_link"),
                       url(r'^send_passwd_reset_link/$', 'accounts_send_passwd_reset_link', name="accounts_send_passwd_reset_link"),
                       url(r'^process_email_confirm/(\d+)/$', 'accounts_process_email_confirm', name="accounts_process_email_confirm"),
                       url(r'^passwd_reset/(\d+)/$', 'accounts_passwd_reset', name="accounts_passwd_reset"),
                       url(r'^passwd_change/$', 'accounts_passwd_change', name="accounts_passwd_change"),
                       )

urlpatterns += patterns('',
                        url(r'^logout/$',
                            'django.contrib.auth.views.logout',
                            {'next_page': '/'}, name="logout"),
                        url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts_login.html'}, name="login"),
                        )
