# -*- coding: utf-8 -*-
from django.conf.urls import *

urlpatterns = patterns('uploader.views',
    url(r'^plot/$', 'upload_response', name='upload_response'),
    url(r'^newplot/$', 'new_plot', name='new_plot'),
    url(r'^dragdropreceive.html$', 'dragdropreceive', name='dragdropreceive'),
)