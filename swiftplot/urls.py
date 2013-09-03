from django.conf.urls import patterns, include, url
from swiftplot.views import index, about, contact
import plots.views as plotviews
#import plots.views as plotviews

from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^graph_display.png$', plotviews.graph_display),
    url(r'^$', index),
    url(r'^index/$', index),
    url(r'^about/$', about),
    url(r'^contact/$', contact),
    url(r'^graph_display.png$', plotviews.graph_display),
    # Examples:
    # url(r'^$', 'swiftplot.views.home', name='home'),
    # url(r'^swiftplot/', include('swiftplot.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
	#url(r'^admin/', include(admin.site.urls)),
	(r'^', include('uploader.urls')),
)
