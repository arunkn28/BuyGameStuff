from django.conf.urls import url
from django.contrib.auth.views import LogoutView

from .views import LoginView, RegisterView

urlpatterns = [
    
    url(r'^login/$', LoginView.as_view(),name='login'),
    url(r'^register/$', RegisterView.as_view(),name='register'),
     url(r'^logout/$', LogoutView.as_view(),name='logout'),
     
]