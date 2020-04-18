from django.contrib import admin
from django.urls import path
from . import views
from products.views import ProductListView
from django.urls import include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('users/login', views.login_site, name='login'),
    path('users/logout', views.logout_site, name='logout'),
    path('users/register', views.register, name='register'),
    path('admin/', admin.site.urls),
    path('products/', include('products.urls')),
    path('cart/', include('cartshop.urls')),
    path('order/', include('orders.urls')),
    path('addresses/', include('shipping_addresses.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, 
                          document_root=settings.MEDIA_ROOT)
