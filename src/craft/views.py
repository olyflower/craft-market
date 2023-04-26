from random import randint

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView

from craft.forms import CheckoutForm, OrderForm
from craft.models import Order, Product


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


class OrderView(LoginRequiredMixin, View):
    login_url = "core:login"
    template_name = "craft/order.html"

    def get(self, request):
        user = request.user
        order = Order.objects.filter(user=user).first()
        if order:
            total = 0
            for product in order.product.all():
                total += product.price

            context = {"order": order, "total": total}
            return render(request, "craft/order.html", context)
        else:
            context = {"message": "You dont have order yet."}
            return render(request, "craft/empty_order.html", context)

    def post(self, request):
        user = request.user
        order = Order.objects.filter(user=user).first()
        if order:
            product_id = request.POST.get("product_id")
            product = Product.objects.get(id=product_id)
            order.product.remove(product)
            order.quantity -= 1
            order.save()
            total = 0
            for product in order.product.all():
                total += product.price

            context = {"order": order, "total": total}
            return render(request, "craft/order.html", context)


class AddToCartView(LoginRequiredMixin, View):
    login_url = "core:login"

    def post(self, request, id):
        form = OrderForm(request.POST)
        if form.is_valid():
            product_id = id
            quantity = form.cleaned_data["quantity"]
            product = Product.objects.get(id=product_id)
            order, created = Order.objects.get_or_create(user=request.user, status="new")
            if not order.order_name:
                order.order_name = randint(10000, 99999)
            order.product.add(product)
            order.quantity += quantity
            order.save()
            return redirect("craft:order")
        else:
            return render(request, "product_list.html", {"form": form})


class CheckoutView(LoginRequiredMixin, View):
    login_url = "core:login"
    template_name = "craft/checkout.html"

    def get(self, request):
        user = request.user
        order = Order.objects.filter(user=user).first()
        if order:
            total = 0
            for product in order.product.all():
                total += product.price

            context = {"order": order, "total": total, "form": CheckoutForm()}
            return render(request, "craft/checkout.html", context)
        else:
            return redirect("craft:order")

    def post(self, request):
        user = request.user
        order = Order.objects.filter(user=user).first()
        if order:
            form = CheckoutForm(request.POST)
            if form.is_valid():
                order.buyer_name = form.cleaned_data["buyer_name"]
                order.buyer_phonenumber = form.cleaned_data["buyer_phonenumber"]
                order.shipping_address = form.cleaned_data["shipping_address"]
                order.payment_method = form.cleaned_data["payment_method"]
                order.save()
                return render(request, "craft/order_success.html")
            else:
                total = 0
                for product in order.product.all():
                    total += product.price

                context = {"order": order, "total": total, "form": form}
                return render(request, "craft/checkout.html", context)
        else:
            return redirect("craft:order")


class OrderSuccessView(View):
    template_name = "craft/order_success.html"
    success_url = reverse_lazy("core:index")


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
