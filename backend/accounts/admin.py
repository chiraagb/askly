from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Notification, Admin, Documents, Organization, OrganizationFile

User = get_user_model()


class CustomUserAdmin(BaseUserAdmin):
    # Define the fieldsets to include the 'email' field when creating a user
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )

    # Define the list_display and fieldsets for user modification
    list_display = ("username", "email", "is_staff", "is_active")
    fieldsets = (
        (
            None,
            {"fields": ("username", "password")},
        ),
        (
            "Personal info",
            {
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "phone_number",
                    "organization",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Important dates",
            {"fields": ("last_login", "date_joined")},
        ),
        (
            "Assistants",
            {"fields": ("assistant_id", "thread_id")},
        ),
    )


# Register the CustomUserAdmin
admin.site.register(User, CustomUserAdmin)
admin.site.register(Notification)
admin.site.register(Documents)
admin.site.register(Admin)
admin.site.register(Organization)
admin.site.register(OrganizationFile)
