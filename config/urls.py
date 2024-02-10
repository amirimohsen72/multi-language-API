from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.i18n import i18n_patterns

from core.api.views import change_lang, change_lang_web

from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="multi language API",
        default_version='v1',
        description="Test api for mobile application edge",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="amirimohsen72@gmail.com"),
        license=openapi.License(name="BSD License"),

    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
)

urlpatterns += [
    # path('api-auth/', include('rest_framework.urls')),

                  path('auth/', include('djoser.urls.authtoken')),
                  path('', include('core.api.urls')),
                  path('shop/', include('shop.api.urls')),
                  path('support/', include('support.api.urls')),

                  path('change_lang/', change_lang, name='change_lang'),
                  path('change_lang_web/', change_lang_web, name='change_lang_Web'),

                  path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
                  path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

                  path('rosetta/', include('rosetta.urls')),
                  # path('api-auth/', include('rest_framework.urls')),
                #   path("__debug__/", include("debug_toolbar.urls")),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
