from django.contrib import admin

from craft.models import (Brand, Cart, CartItem, Category, Order, OrderItem,
                          Product)


class ProductAdminInline(admin.StackedInline):
    model = Product


class CartItemAdminInline(admin.StackedInline):
    model = CartItem


class OrderItemAdminInline(admin.StackedInline):
    model = OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    inlines = [ProductAdminInline]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    inlines = [ProductAdminInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "in_stock", "discount", "category", "brand", "quantity")
    list_filter = ("category", "brand")
    search_fields = ("name__istartswith",)
    actions = ["set_discount_10", "set_discount_0"]

    def set_discount_10(self, request, queryset):
        discount_value = 10
        queryset.update(discount=discount_value)

    set_discount_10.short_description = "Set discount 10 percent for selected products"

    def set_discount_0(self, request, queryset):
        discount_value = 0
        queryset.update(discount=discount_value)

    set_discount_0.short_description = "Set discount 0 for selected products"


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "quantity", "price")
    inlines = [CartItemAdminInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "product", "quantity", "price")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_name", "user", "status", "quantity", "order_price")
    list_filter = ("status",)
    date_hierarchy = "create_datetime"
    inlines = [OrderItemAdminInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "price")
