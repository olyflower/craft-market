from django.urls import include, path
from rest_framework import routers

from api.views import CustomerViewSet, ProductListView

app_name = "api"
router = routers.DefaultRouter()
router.register("customers", CustomerViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("craft/products/", ProductListView.as_view(), name="product_list"),
]
