from django.contrib import admin
from modules.models import Module, Subscription, Lesson


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    """Админка модулей"""
    list_display = ('serial_number', 'title', 'description', 'owner', 'last_update', 'is_published')
    search_fields = ('serial_number', 'title', 'description', 'last_update', 'owner')
    list_filter = ('title', 'description', 'owner')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Админка уроков"""
    list_display = ('module', 'title', 'description', 'video_link', 'owner')
    search_fields = ('module', 'title', 'description', 'video_link', 'owner')
    list_filter = ('module', 'title', 'description', 'video_link', 'owner')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Админка подписок"""
    list_display = ('user', 'module')
    search_fields = ('user', 'module')
    list_filter = ('user', 'module')