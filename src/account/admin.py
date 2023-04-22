from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


@admin.register(get_user_model())
class CustomerAdmin(UserAdmin):
    ordering = ("first_name", "last_name")
    list_display_links = ("email",)
    readonly_fields = ("email",)
    fields = ("first_name", "last_name", "password", "email", "phone_number", "birth_date", "photo", "city")
    list_display = ("get_full_name", "email", "phone_number", "birth_date", "city")
    search_fields = ("first_name__istartswith", "last_name__istartswith")
    fieldsets = None
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "email",
                ),
            },
        ),
    )
