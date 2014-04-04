from django.conf.urls import patterns, url, include
from django.conf import settings

urlpatterns = patterns('',
                       url(r'^', include('cityproblems.site.urls')),
                       url(r'^accounts/', include('cityproblems.accounts.urls')),
                       url(r'^admin/', include('cityproblems.admin.urls')),
                       url(r'^files/', include('cityproblems.files.urls')),
                       url(r'^comments/', include('cityproblems.comments.urls')),
                       )


# media files
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)