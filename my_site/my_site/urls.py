from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap

import debug_toolbar

from general_logic.sitemaps import PostSitemap


sitemaps = {'posts': PostSitemap,}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('general_logic.urls', namespace='general_logic')),
    path('english/', include('english.urls', namespace='english')),

    path('__debug__/', include(debug_toolbar.urls)),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('social-auth/', include('social_django.urls', namespace='social')),
]

# Это сделано специально, стобы тестовый сервер мог отрабатывать фотки. На продакшнене этим займется реальный вебсервер
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.MUSIC_URL, document_root=settings.MUSIC_ROOT)
