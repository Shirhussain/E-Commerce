from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

from home import views

urlpatterns = [
    path('selectlanguage', views.selectlanguage, name='selectlanguage'),
    path('selectcurrency', views.selectcurrency, name='selectcurrency'),
    path('savelangcur', views.savelangcur, name='savelangcur'),
    path('i18n/', include('django.conf.urls.i18n')),
]



urlpatterns += i18n_patterns (
    path('', include('home.urls', namespace='home')),
    path(_('product/'), include('product.urls', namespace='product')),
    path(_('order/'), include('order.urls', namespace='order')),
    path(_('user/'), include('user.urls', namespace='user')),
    path(_('admin/'), admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    prefix_default_language=False,
)

if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)