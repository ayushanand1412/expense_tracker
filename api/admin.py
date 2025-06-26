from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Expense

# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'name', 'phone', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    ordering = ('email',)
    search_fields = ('email', 'name')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Timestamps', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'phone', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'category', 'date')
    list_filter = ('category', 'date')
    search_fields = ('user__email', 'category')
