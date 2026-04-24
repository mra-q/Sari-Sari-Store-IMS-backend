from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def root_view(request):
    return JsonResponse({
        'message': 'Inventory Management System API',
        'status': 'running',
        'endpoints': {
            'admin': '/admin/',
            'api': '/api/',
            'auth': '/api/auth/',
            'products': '/api/products/',
            'inventory': '/api/inventory/',
            'stock': '/api/stock/',
        }
    }, json_dumps_params={'indent': 2})

urlpatterns = [
    path('', root_view),
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.users.urls')),
    path('api/products/', include('apps.products.urls')),
    path('api/inventory/', include('apps.inventory.urls')),
    path('api/stock/', include('apps.stock.urls')),
    path('api/sync/', include('apps.sync.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
