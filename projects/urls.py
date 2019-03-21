from django.conf.urls import url

from projects.views import manage_group, create_project, affect_user, configure_project, archive_project, edit_project, \
    block_member

urlpatterns = [
    url(r'^archive-project/(?P<project_id>\d+)/$', archive_project, name='archive-project'),
    url(r'^$', manage_group, name='manage-group'),
    url(r'^create-project/$', create_project, name='create-project'),
    url(r'^edit-project/(?P<project_id>\d+)/$', edit_project, name='edit-project'),
    url(r'^block-member/(?P<project_id>\d+)/(?P<member>[\w.@+-]+)/$', block_member, name='block-member'),
    url(r'^users-affectation/$', affect_user, name='users-affectation'),
    url(r'^configure-project/(?P<project_id>\d+)/(?P<user>[\w.@+-]+)/$', configure_project, name='configure-project'),
]

