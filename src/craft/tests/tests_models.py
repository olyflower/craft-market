from django.core.exceptions import ValidationError
from django.test import TestCase

from craft.models import Brand, Category, Product


class TestCraftModel(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Name Category")
        self.brand = Brand.objects.create(name="Name Brand")
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Product Description",
            price=19.99,
            discount=10.00,
            category=self.category,
            brand=self.brand,
            quantity=50,
        )

    def test_category_name_max_length(self):
        with self.assertRaises(ValidationError):
            category = Category(name="A" * 7000)
            category.full_clean()

    def test_product_with_params(self):
        self.assertEqual(self.product.brand, self.brand)
