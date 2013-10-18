from django.conf.urls import patterns, include, url
import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ServiSoft.views.home', name='home'),
    # url(r'^ServiSoft/', include('ServiSoft.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^', include('ServiSoft.apps.home.urls')),
    url(r'^', include('ServiSoft.apps.mocel.urls')),
    url(r'^', include('ServiSoft.apps.webServices.wsProductos.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT}),
)
