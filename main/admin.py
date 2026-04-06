from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin

from .models import Product


admin.site.site_header = "BestLogs Admin"
admin.site.site_title = "BestLogs Portal"
admin.site.index_title = "Manage BestLogs"


# Safely unregister default models
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

try:
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass


# =========================
# USER ADMIN
# =========================
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "is_staff", "is_active")
    search_fields = ("username", "email")
    list_filter = ("is_staff", "is_active")
    ordering = ("username",)

    # Allow changing so add-user and password pages work
    def has_change_permission(self, request, obj=None):
        return True

    # Optional: block delete
    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(User, CustomUserAdmin)


# =========================
# PRODUCT ADMIN
# =========================
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "platform",
        "account_year",
        "account_type",
        "followers",
        "stock",
        "price",
        "created_at",
    )
    list_filter = ("platform", "account_type", "account_year")
    search_fields = ("name",)
    ordering = ("-created_at",)

    # Allow change so product editing works
    def has_change_permission(self, request, obj=None):
        return True

    # Optional: block delete
    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Product, ProductAdmin)
