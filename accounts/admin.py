from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.
class CustomUserAdmin(UserAdmin):
    # setting filds of what to showing in admin-dashboard
    model = User
    list_display = ("email","id" , "is_superuser", "is_active", "created_date")
    list_filter = ("email", "is_superuser", "is_active", "created_date")
    search_fields = ("email",)
    ordering = ("created_date",)
    fieldsets = (
        ('Authentication', {
            'fields': (
                "email", "password"
            ),
        }),
        ('Permissions', {
            'fields': (
                "is_staff", "is_active","is_superuser"
            ),
        }),
    )
    # setting fields for adding and save new User by admin-dashboard
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "is_superuser"
            )}
        ),
    )

admin.site.register(User, CustomUserAdmin)
