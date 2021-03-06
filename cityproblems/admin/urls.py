from django.conf.urls import patterns, include, url

from .views import UsersList, ProblemCategoriesList,\
    ProblemCategoryCreate, ProblemCategoryEdit,\
    ProblemCategoryDelete

urlpatterns = patterns('cityproblems.admin.views',
                       url(r'^$', 'admin_home', name='admin_home'),
                       url(r'^addAdmin/$', 'add_admin', name='admin_addAdmin'),
                       url(r'^addParameter/$', 'add_parameter', name='admin_addParameter'),
                       url(r'^editParameter/(\d+)/$', 'edit_parameter', name='admin_editParameter'),
                       url(r'^adminsList/$', 'admins_list', name='admin_adminsList'),
                       url(r'^parametersList/$', 'parameters_list', name='admin_parametersList'),
                       url(r'^processLock/$', 'process_lock', name='admin_processLock'),
                       url(r'^processAdminRemove/$', 'process_admin_remove', name='admin_processAdminRemove'),
                       url(r'^processParameterRemove/$', 'process_parameter_remove', name='admin_processParameterRemove'),
                       url(r'^changePasswd/(\d+)/$', 'change_passwd', name='admin_changePasswd'),
                       )

urlpatterns += patterns('',
                        url(r'^users/$', UsersList.as_view(), name='admin_UsersList'),
                        url(r'^users/(?P<page>\d+)/$', UsersList.as_view(), name='admin_UsersList'),
                        url(r'^categories/$', ProblemCategoriesList.as_view(), name='admin_ProblemCategoriesList'),
                        url(r'^create/category/$', ProblemCategoryCreate.as_view(), name='admin_ProblemCategoryCreate'),
                        url(r'^edit/category/(?P<pk>\d+)/$', ProblemCategoryEdit.as_view(), name='admin_ProblemCategoryEdit'),
                        url(r'^delete/category/(?P<pk>\d+)/$', ProblemCategoryDelete.as_view(), name='admin_ProblemCategoryDelete'),
                        )