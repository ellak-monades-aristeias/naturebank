from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib.gis import admin

admin.autodiscover()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("naturebank.urls")),
    path("", include("django.contrib.flatpages.urls")),
]

if settings.DEBUG:
    urlpatterns = (
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + urlpatterns
    )
