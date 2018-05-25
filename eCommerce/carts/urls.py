from django.conf.urls import url

from .views import UpdateCart, CartView

urlpatterns = [
    url(r'^$', CartView.as_view(),name='cartview'),
    url(r'^updatecart/$', UpdateCart.as_view(),name='updatecart')
    #url(r'^cart/$', ProductDetail.as_view(),name='productdetails'),
]