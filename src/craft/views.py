import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView

from craft.forms import OrderForm
from craft.models import Cart, CartItem, Order, OrderItem, Product


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


class SaleListView(ListView):
    model = Product
    template_name = "craft/sale.html"
    context_object_name = "sale"

    def get_queryset(self):
        return super().get_queryset().exclude(discount=0)


def contacts(request):
    return render(request, "craft/contacts.html")


def about(request):
    return render(request, "craft/about.html")


def payment_delivery(request):
    return render(request, "craft/payment_delivery.html")


def update_cart(cart):
    aggregate_sum = cart.cart_items.aggregate(quantity=Sum("quantity"), price=Sum("price"))
    cart.quantity = aggregate_sum["quantity"] or 0
    cart.price = aggregate_sum["price"] or 0
    cart.save()


class CartAddProduct(LoginRequiredMixin, View):
    login_url = reverse_lazy("core:login")

    def post(self, request, *args, **kwargs):
        product_id = kwargs.get("product_id")
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product = Product.objects.get(id=product_id)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product=product, defaults={"price": product.price}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.price = product.price * cart_item.quantity
            cart_item.save()
        update_cart(cart)
        next_url = request.GET.get("next")
        if next_url:
            return HttpResponseRedirect(next_url)
        else:
            return HttpResponseRedirect(reverse("craft:cart"))


class CartView(LoginRequiredMixin, TemplateView):
    template_name = "craft/cart.html"
    model = CartItem
    login_url = reverse_lazy("core:login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        context["cart_items"] = cart.cart_items.all()
        context["cart_price"] = cart.price
        return context

    def post(self, request, *args, **kwargs):
        product_id = request.POST.get("product_id")
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product = Product.objects.get(id=product_id)
        CartItem.objects.get_or_create(cart=cart, product=product, defaults={"price": product.price})
        update_cart(cart)
        return HttpResponseRedirect(reverse("craft:cart"))


class CartItemDeleteView(LoginRequiredMixin, View):
    login_url = reverse_lazy("core:login")

    def get(self, request, *args, **kwargs):
        item_id = kwargs["item_id"]
        cart_item = CartItem.objects.get(id=item_id)
        cart = cart_item.cart
        cart_item.delete()
        update_cart(cart)
        return HttpResponseRedirect(reverse("craft:cart"))


class OrderView(View):
    def get(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        form = OrderForm()
        context = {"form": form, "cart": cart}
        return render(request, "craft/order.html", context)

    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.quantity = cart.quantity
            order.order_price = cart.price
            order.order_name = str(random.randint(10000, 99999))
            order.save()
            order_items = [
                OrderItem(order=order, product=item.product, quantity=item.quantity, price=item.price)
                for item in cart.cart_items.all()
            ]
            OrderItem.objects.bulk_create(order_items)
            cart.cart_items.all().delete()
            cart.price = 0
            cart.save()
            return redirect(reverse("craft:order_success", kwargs={"order_id": order.pk}))
        context = {"form": form, "cart": cart}
        return render(request, "craft/order.html", context)


class OrderDetailView(View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id, user=request.user)
        order_items = order.order_items.all()
        context = {"order": order, "order_items": order_items}
        return render(request, "craft/order_success.html", context)
