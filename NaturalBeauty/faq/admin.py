from django.contrib import admin
from django.contrib.auth.models import Permission

from .models import Category, Question, Response


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['id']
    list_display = ['id', 'name']
    list_filter = ('name',)


@admin.register(Question)
class AdminAdmin(admin.ModelAdmin):
    search_fields = ['id']
    list_display = ['id', 'question']
    list_filter = ('question',)


@admin.register(Response)
class AdminAdmin(admin.ModelAdmin):
    search_fields = ['id']
    list_display = ['id', 'response']
    list_filter = ('response',)


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'content_type',
        'codename',
    )
    list_filter = ('content_type',)
    search_fields = ['codename', 'name']

# EOF
