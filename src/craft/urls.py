from django.urls import path

from craft.views import (CartAddProduct, CartView, GetProductsView,
                         ProductDetailView, about, contacts, payment_delivery,
                         sale, CartItemDeleteView)

app_name = "craft"

urlpatterns = [
    path("products-list/", GetProductsView.as_view(), name="get_products"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("sale/", sale, name="sale"),
    path("contacts/", contacts, name="contacts"),
    path("about/", about, name="about"),
    path("payment-delivery/", payment_delivery, name="payment_delivery"),
    path("add-to-cart/<int:product_id>/", CartAddProduct.as_view(), name="add_to_cart"),
    path("delete-item/<int:item_id>/", CartItemDeleteView.as_view(), name="delete_item"),
    path("cart/", CartView.as_view(), name="cart"),
]
