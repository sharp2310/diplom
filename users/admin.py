from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'phone', 'telegram_id', 'is_active')
    list_display_links = ('email', 'phone', 'telegram_id')