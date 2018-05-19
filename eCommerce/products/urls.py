from django.conf.urls import url

from .views import ProductList, ProductDetail

urlpatterns = [
    url(r'^productlist/$', ProductList.as_view(),name='productlist'),
    url(r'^productdetails/(?P<slug>[\w-]+)/$', ProductDetail.as_view(),name='productdetails'),
]