from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from craft.models import Brand, Category, Order, Product


class ProductAdminInline(admin.StackedInline):
    model = Product


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
    # actions = ["discount_10", "discount_0"]
    #
    # @admin.action(description="Set discount 10%")
    # def discount_10(self, request, queryset):
    #     queryset.update(discount=10)
    #
    # @admin.action(description="Set discount 0%")
    # def discount_0(self, request, queryset):
    #     queryset.update(discount=0)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "status", "quantity", "product_count", "links_to_products")
    list_filter = ("status",)
    date_hierarchy = "create_datetime"

    def product_count(self, obj):
        if obj.product:
            return obj.product.count()
        return 0

    def links_to_products(self, obj):
        if obj.product:
            products = obj.product.all()
            links = []
            for product in products:
                links.append(
                    f"<a class='button' href='{reverse('admin:craft_product_change', args=[product.pk])}'"
                    f">{product.name}</a>"
                )
            return format_html("</br></br>".join(links))
        return "No products found"
