from django.db.models import Q
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from craft.models import Product


class GetProductsView(ListView):
    redirect_field_name = "index"
    template_name = "craft/products_list.html"
    model = Product

    def get_queryset(self):
        search = self.request.GET.get("search_text")
        search_fields = ["name", "category__name", "brand__name"]
        if search:
            or_filter = Q()
            for field in search_fields:
                or_filter |= Q(**({f"{field}__istartswith": search}))
            return Product.objects.filter(or_filter)

        return Product.objects.all()


class ProductDetailView(DetailView):
    redirect_field_name = "index"
    template_name = "craft/product_detail.html"
    model = Product


def sale(request):
    products_in_sale = Product.objects.exclude(discount=0)
    context = {"products_in_sale": products_in_sale}
    return render(request, "craft/sale.html", context)


def contacts(request):
    return render(request, "craft/contacts.html")


def about(request):
    return render(request, "craft/about.html")


def payment_delivery(request):
    return render(request, "craft/payment_delivery.html")
