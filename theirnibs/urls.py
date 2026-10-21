from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url='/static/images/favicon.ico?v=crown2026', permanent=False)),
    path('admin/', admin.site.urls),
    path('admin-panel/', include('admin_panel.urls', namespace='admin_panel')),
    path('seller-panel/', include('seller_panel.urls', namespace='seller_panel')),
    path('product-catalog/', include('product.urls', namespace='product')),
    path('', include('store.urls')),
]

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

