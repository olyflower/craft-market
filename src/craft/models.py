import random

from _decimal import Decimal
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from faker import Faker
from phonenumber_field.modelfields import PhoneNumberField


class BaseModel(models.Model):
    class Meta:
        abstract = True

    create_datetime = models.DateTimeField(null=True, auto_now_add=True)
    last_update = models.DateTimeField(null=True, auto_now=True)


class Category(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="category/", blank=True, null=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    @classmethod
    def generate_instances(cls, count):
        faker = Faker()
        for _ in range(count):
            cls.objects.create(
                name=faker.word(),
            )


class Brand(BaseModel):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="brand/", null=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @classmethod
    def generate_instances(cls, count):
        faker = Faker()
        for _ in range(count):
            cls.objects.create(
                name=faker.word(),
            )


class Product(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="product/", blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    in_stock = models.BooleanField(default=True)
    category = models.ForeignKey(to="craft.Category", related_name="products", on_delete=models.CASCADE)
    brand = models.ForeignKey(to="craft.Brand", related_name="products", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0, null=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.brand.name}{self.category.name})"

    def price_with_discount(self):
        if self.discount is not None:
            discount_decimal = Decimal(str(self.discount))
            price_decimal = Decimal(str(self.price))
            discounted_price = price_decimal * (1 - discount_decimal / 100)
            return "{:.2f}".format(discounted_price)
        else:
            return "{:.2f}".format(self.price)

    @classmethod
    def generate_instances(cls, count):
        faker = Faker()
        for _ in range(count):
            cls.objects.create(
                name=faker.word(),
                description=faker.sentence(),
                price=faker.pydecimal(left_digits=2, right_digits=2, positive=True),
                discount=random.randint(0, 25),
                in_stock=faker.boolean(),
                category=Category.objects.order_by("?").first(),
                brand=Brand.objects.order_by("?").first(),
                quantity=random.randint(1, 100),
            )


class Favourite(BaseModel):
    user = models.ForeignKey(to=get_user_model(), related_name="favourites", on_delete=models.CASCADE)
    product = models.ForeignKey(to="craft.Product", related_name="favourite_product", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "product")


class Cart(BaseModel):
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)


class CartItem(BaseModel):
    cart = models.ForeignKey(to="craft.Cart", related_name="cart_items", on_delete=models.CASCADE)
    product = models.ForeignKey(to="craft.Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        unique_together = ("cart", "product")

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def total(self):
        return self.price * self.quantity


class Order(BaseModel):
    STATUS_CHOICES = (
        ("new", "New"),
        ("in_progress", "In progress"),
        ("completed", "Completed"),
    )
    PAYMENT_METHOD_CHOICES = (("google_pay", "Google Pay"), ("paypal", "PayPal"))
    order_name = models.PositiveIntegerField(default=0, blank=False)
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    buyer_name = models.CharField(max_length=100)
    buyer_phonenumber = PhoneNumberField(_("phone number"))
    shipping_address = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=100, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    quantity = models.PositiveIntegerField(default=0)
    order_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    class Meta:
        ordering = ["user"]

    def __str__(self):
        return str(self.order_name)


class OrderItem(BaseModel):
    order = models.ForeignKey(to="craft.Order", related_name="order_items", on_delete=models.CASCADE)
    product = models.ForeignKey(to="craft.Product", related_name="ordered_in", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
