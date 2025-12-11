from django.contrib import admin
from .models import CorePillar, Service

@admin.register(CorePillar)
class CorePillarAdmin(admin.ModelAdmin):
    list_display = ('order', 'title')
    list_display_links = ('title',)
    search_fields = ('title',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
