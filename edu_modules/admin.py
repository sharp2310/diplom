from django.contrib import admin
from edu_modules.models import Module


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'author')
    list_display_links = ('title', 'author')