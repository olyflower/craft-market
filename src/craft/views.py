from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView

from craft.models import Cart, CartItem, Product


class GetProductsView(ListView):
    redirect_name = "index"
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


class CartAddProduct(View):
    def post(self, request, *args, **kwargs):
        product_id = kwargs.get("product_id")
        cart = Cart.objects.get_or_create(user=request.user)[0]
        product = Product.objects.get(id=product_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={"price": product.price})
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        cart.quantity = sum([item.quantity for item in cart.cart_items.all()])
        cart.price = sum([item.total for item in cart.cart_items.all()])
        cart.save()
        return HttpResponseRedirect(reverse("craft:cart"))


class CartView(LoginRequiredMixin, TemplateView):
    template_name = "craft/cart.html"
    model = CartItem
    login_url = reverse_lazy("core:login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        cart = Cart.objects.get_or_create(user=user)[0]
        context["cart_items"] = cart.cart_items.all()
        context["cart_total"] = cart.price
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy("login"))
        product_id = request.POST.get("product_id")
        cart = Cart.objects.get_or_create(user=request.user)[0]
        product = Product.objects.get(id=product_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={"price": product.price})
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        cart.quantity = sum([item.quantity for item in cart.cart_items.all()])
        cart.price = sum([item.total for item in cart.cart_items.all()])
        cart.save()
        return HttpResponseRedirect(reverse("craft:cart"))


class CartItemDeleteView(LoginRequiredMixin, View):
    login_url = reverse_lazy("core:login")

    def get(self, request, *args, **kwargs):
        item_id = kwargs["item_id"]
        cart_item = CartItem.objects.get(id=item_id)
        cart = cart_item.cart
        cart_item.delete()
        cart.quantity = sum([item.quantity for item in cart.cart_items.all()])
        cart.price = sum([item.total for item in cart.cart_items.all()])
        cart.save()
        return HttpResponseRedirect(reverse("craft:cart"))