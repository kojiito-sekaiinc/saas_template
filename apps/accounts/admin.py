from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Profile, User


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    readonly_fields = ("created_at", "updated_at")


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("email", "is_active", "is_staff", "created_at")
    list_filter = ("is_active", "is_staff")
    search_fields = ("email",)
    ordering = ("-created_at",)
    inlines = [ProfileInline]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )
    add_fieldsets = (
        (None, {"fields": ("email", "password1", "password2")}),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "free_until", "is_in_free_trial", "created_at")
    list_filter = ("free_until",)
    search_fields = ("user__email",)
    readonly_fields = ("created_at", "updated_at")
    raw_id_fields = ("user",)

    @admin.display(boolean=True, description="In Free Trial")
    def is_in_free_trial(self, obj):
        return obj.is_in_free_trial
