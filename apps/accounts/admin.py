from django.contrib import admin
from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin
from apps.accounts.models import Account, OtpModel, NotificationModel


#comment

@register(Account)
class AccountsAdmin(UserAdmin):
    """admin panel to manage users """
    list_display = (
        'phone_number', 'id', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'date_joined','email',
    )
    # list_filter = ('is_speaker')
    search_fields = ('id', 'phone_number', 'email', 'first_name',)
    date_hierarchy = 'date_joined'
    ordering = ['-date_joined', 'id']
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        # (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_admin",
                    "is_superuser",
                    "groups",
                    "user_permissions", 'first_name', 'last_name','email',
                ),
            },
        ),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2'),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.set_password(form.cleaned_data['password1'])
        super().save_model(request, obj, form, change)


admin.site.register(OtpModel)
admin.site.register(NotificationModel)