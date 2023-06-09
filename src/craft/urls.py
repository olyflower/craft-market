from django.urls import path

from craft.views import (AddToFavoritesView, CartAddProduct,
                         CartItemDeleteView, CartView, FavoritesView,
                         GetProductsView, OrderDetailView, OrderView,
                         ProductDetailView, RemoveFromFavourites, SaleListView,
                         about, contacts, payment_delivery)

app_name = "craft"

urlpatterns = [
    path("products-list/", GetProductsView.as_view(), name="get_products"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("sale", SaleListView.as_view(), name="sale"),
    path("favourites", FavoritesView.as_view(), name="favourites"),
    path("add-to-favourites/<int:product_id>/", AddToFavoritesView.as_view(), name="add_to_favourites"),
    path("remove-from-favourites/<int:pk>/", RemoveFromFavourites.as_view(), name="remove_from_favourites"),
    path("contacts/", contacts, name="contacts"),
    path("about/", about, name="about"),
    path("payment-delivery/", payment_delivery, name="payment_delivery"),
    path("add-to-cart/<int:product_id>/", CartAddProduct.as_view(), name="add_to_cart"),
    path("delete-item/<int:item_id>/", CartItemDeleteView.as_view(), name="delete_item"),
    path("cart/", CartView.as_view(), name="cart"),
    path("order/", OrderView.as_view(), name="order"),
    path("order-success/<int:order_id>/", OrderDetailView.as_view(), name="order_success"),
]
