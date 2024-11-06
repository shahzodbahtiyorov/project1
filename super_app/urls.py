from decouple import config
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from dotenv import load_dotenv
import os
from django.urls import path


def trigger_error(request):
    division_by_zero = 1 / 0


load_dotenv()
schema_view = get_schema_view(
    openapi.Info(
        title="API Docs",
        default_version='v1',
        description="Super App",
        terms_of_service="",
        contact=openapi.Contact(url="t.me/n1nurmuhammad", name="Nurmuhammad N"),
        license=openapi.License(name="BSD License"),
    ),

    public=True,
    # permission_classes=(permissions.IsAdminUser,)
    #cors add 
    #cors add

    url=("https://superapp-test.cloudgate.uz/"),
    # url=os.getenv("http://localhost:8000")
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("api.urls")),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('account/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('account/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('sentry-debug/', trigger_error),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
