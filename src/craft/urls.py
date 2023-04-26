from django.urls import path

from craft.views import (AddToCartView, CheckoutView, GetProductsView,
                         OrderView, ProductDetailView, about, contacts,
                         payment_delivery, sale, OrderSuccessView)

app_name = "craft"

urlpatterns = [
    path("products-list/", GetProductsView.as_view(), name="get_products"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("sale/", sale, name="sale"),
    path("contacts/", contacts, name="contacts"),
    path("about/", about, name="about"),
    path("payment-delivery/", payment_delivery, name="payment_delivery"),
    path("order/", OrderView.as_view(), name="order"),
    path("add-to-cart/<int:id>/", AddToCartView.as_view(), name="add_to_cart"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("order-success/", OrderSuccessView.as_view(), name="order_success")
]
