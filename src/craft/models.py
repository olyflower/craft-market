from django.contrib.auth import get_user_model
from django.db import models
from faker import Faker


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
    quantity = models.PositiveIntegerField(blank=False, null=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.brand.name}{self.category.name})"

    @classmethod
    def generate_instances(cls, count):
        faker = Faker()
        for _ in range(count):
            cls.objects.create(
                name=faker.word(),
                description=faker.sentence(),
                price=faker.pydecimal(left_digits=2, right_digits=2, positive=True),
                discount=faker.random_int(min=0, max=50),
                in_stock=faker.boolean(),
                category=Category.objects.order_by("?").first(),
                brand=Brand.objects.order_by("?").first(),
                quantity=faker.random_int(min=1, max=500),
            )


class Order(BaseModel):
    STATUS_CHOICES = (
        ("new", "New"),
        ("in_progress", "In progress"),
        ("completed", "Completed"),
    )
    name = models.PositiveIntegerField(null=False, blank=False)
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    product = models.ManyToManyField(to="craft.Product", related_name="order_products")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    quantity = models.PositiveIntegerField(null=False, blank=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return str(self.name)

    @classmethod
    def generate_instances(cls, count):
        faker = Faker()
        for _ in range(count):
            order = cls.objects.create(
                name=faker.random_number(digits=6),
                user=get_user_model().objects.order_by("?").first(),
                status=faker.random_element(elements=("new", "in_progress", "completed")),
                quantity=faker.random_int(min=1, max=100),
            )
            order.product.set([Product.objects.order_by("?").first()])
