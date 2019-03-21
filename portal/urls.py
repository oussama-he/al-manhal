from django.conf.urls import url

from accounts.views import sidebar
from .views import home, display_publications, create_resource, create_comment, extension_view, rate_resource, get_rating, \
    get_publication_meta_data, archive_publication, edit_resource, extension_view

urlpatterns = [
    url('^home/$', home, name='home'),
    url('^sidebar/$', sidebar, name='sidebar'),
    url('^publications/$', display_publications, name='publications'),
    url('^create-resource/(?P<source>[\w.@+-]+)/$', create_resource, name='create-resource'),
    url('^edit-resource/(?P<pub_id>\d+)/(?P<source>[\w.@+-]+)/$', edit_resource, name='edit-resource'),
    url('^create-comment/(?P<pub_id>\d+)/$', create_comment, name='create-comment'),
    url('^rate-publication/$', rate_resource, name='rate-publication'),
    url('^get-rating/(?P<pub_id>\d+)/$', get_rating, name='get-rating'),
    url('^get-publication-meta-data/(?P<pub_id>\d+)/(?P<user>[\w.@+-]+)/$', get_publication_meta_data, name='get-publication-meta-data'),
    url('^archive-publication/(?P<pub_id>\d+)/$', archive_publication, name='archive-publication'),
    url('^extension/$', extension_view, name='extension'),
]
