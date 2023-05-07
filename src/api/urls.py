from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from api.views import CustomerViewSet, ProductListView

app_name = "api"
router = routers.DefaultRouter()
router.register("customers", CustomerViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Craft-Market API",
        default_version="v1",
        description="API for those who love craft things",
        term_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="admin@admin.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("djoser.urls.jwt")),
    path("docs/", schema_view.with_ui("redoc", cache_timeout=0), name="swagger_docs"),
    path("craft/products/", ProductListView.as_view(), name="product_list"),
]
