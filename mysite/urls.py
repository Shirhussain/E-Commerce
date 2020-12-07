from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # path('', include('home.urls')),
    path('', include('home.urls', namespace='home')),
    path('product/', include('product.urls', namespace='product')),
    path('order/', include('order.urls', namespace='order')),
    path('user/', include('user.urls', namespace='user')),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)