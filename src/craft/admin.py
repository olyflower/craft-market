from django.contrib import admin

from craft.models import Brand, Category, Order, Product

admin.site.register([Category, Brand, Product, Order])
