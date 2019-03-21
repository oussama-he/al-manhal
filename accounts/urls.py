from django.conf.urls import url
from .views import overview, edit_profile, logout_view, change_user_avatar, sign_in_view, \
    sign_up_view, check_status
from django.contrib.auth.views import LoginView

urlpatterns = [
    url(r'^(?P<username>[\w.@+-]+)/overview/$', overview, name='overview'),
    url(r'^(?P<username>[\w.@+-]+)/edit-profile/$', edit_profile, name='edit-profile'),
    url(r'^sign-in/$', sign_in_view, name='sign_in'),
    url(r'^sign-up/$', sign_up_view, name='sign_up'),
    url(r'^login/$', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^change-avatar/$', change_user_avatar, name='change-user-avatar'),
    url(r'^check-status/$', check_status, name='check-status'),
]