from django.conf.urls import url
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView,\
                                       PasswordResetConfirmView, PasswordResetCompleteView 

from .views import LoginView, RegisterView, UpdateAddress

urlpatterns = [
    
    url(r'^login/$', LoginView.as_view(),name='login'),
    url(r'^register/$', RegisterView.as_view(),name='register'),
    url(r'^logout/$', LogoutView.as_view(),name='logout'),
    url(r'^updateaddress/$', UpdateAddress.as_view(),name='updateaddress'),
    url(r'^password_reset/$',
        PasswordResetView.as_view(template_name='password/forgot-password.html',
                                  success_url=reverse_lazy('account:password_reset_done')),
                                  name='password_reset'),
    url(r'^password_reset/done/$',
        PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'),
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmView.as_view(template_name='password/password_reset_confirm.html',
                                         success_url = reverse_lazy('account:password_reset_complete')),
                                        name='password_reset_confirm'),
    url(r'^reset/done/$',
        PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'),
        name='password_reset_complete'),
]