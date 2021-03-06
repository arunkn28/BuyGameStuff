"""eCommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from .account.urls import urlpatterns as account_urls
from .products.urls import urlpatterns as product_urls
from .carts.urls import urlpatterns as cart_urls
from .orders.urls import urlpatterns as order_urls

from .core.views import HomePage

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomePage.as_view(),name='homepage'),
    
    url(r'^account/', include(account_urls, namespace='account')),
    url(r'^product/', include(product_urls, namespace='product')),
    url(r'^cart/', include(cart_urls, namespace='cart')),
    url(r'^order/', include(order_urls, namespace='order')),
    
]

handler404 = 'eCommerce.views.page_not_found_custom'    
handler500 = 'eCommerce.views.page_error_found_custom' 

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)