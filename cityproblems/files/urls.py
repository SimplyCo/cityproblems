from django.conf.urls import patterns, include, url

urlpatterns = patterns('cityproblems.files.views',
                       url(r'^process_upload/$', 'process_upload', name='files_process_upload'),
                       url(r'^process_file_remove/$', 'process_file_remove', name='files_process_file_remove'),
                       )

