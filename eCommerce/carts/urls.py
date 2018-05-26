from django.conf.urls import url

from .views import UpdateCart, CartView, GetCartCount

urlpatterns = [
    url(r'^$', CartView.as_view(),name='cartview'),
    url(r'^updatecart/$', UpdateCart.as_view(),name='updatecart'),
    url(r'^cartcount/$', GetCartCount.as_view(),name='cartcount'),
]