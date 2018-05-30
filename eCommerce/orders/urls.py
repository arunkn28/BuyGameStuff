from django.conf.urls import url

from .views import OrderView

urlpatterns = [
    url(r'^$', OrderView.as_view(),name='orderview'),
    #url(r'^updatecart/$', UpdateCart.as_view(),name='updatecart'),
    #url(r'^cartcount/$', GetCartCount.as_view(),name='cartcount'),
]