
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),  
    path('account/', include('account.urls')),
    path('adminpanel/', include('admin_panel.urls')),
    path('payment/', include('payment.urls')),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


