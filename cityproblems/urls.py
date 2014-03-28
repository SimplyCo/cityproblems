from django.conf.urls import patterns, url, include
from django.conf import settings

urlpatterns = patterns('',
                       url(r'^$', 'cityproblems.site.views.home', name='home'),
                       url(r'^$', 'cityproblems.site.views.no_permissions', name='no_permissions'),
                       url(r'^accounts/', include('cityproblems.accounts.urls')),
                       url(r'^admin/', include('cityproblems.admin.urls')),
                       )


# media files
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)