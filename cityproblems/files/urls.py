from django.conf.urls import patterns, include, url

urlpatterns = patterns('cityproblems.files.views',
                       url(r'^process_upload/$', 'process_upload', name='files_process_upload'),
                       url(r'^process_file_remove/$', 'process_file_remove', name='files_process_file_remove'),
                       url(r'^process_image_move/$', 'process_image_move', name='files_process_image_move'),
                       )

