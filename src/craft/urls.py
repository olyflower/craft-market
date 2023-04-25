from django.urls import path

from craft.views import (GetProductsView, OrderView, ProductDetailView, about,
                         add_to_cart, contacts, payment_delivery, sale)

app_name = "craft"

urlpatterns = [
    path("products-list/", GetProductsView.as_view(), name="get_products"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("sale/", sale, name="sale"),
    path("contacts/", contacts, name="contacts"),
    path("about/", about, name="about"),
    path("payment-delivery/", payment_delivery, name="payment_delivery"),
    path("order/", OrderView.as_view(), name="order"),
    path("add-to-cart/<int:id>/", add_to_cart, name="add_to_cart"),
]
