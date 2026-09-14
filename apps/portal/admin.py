from django.contrib import admin
from .models import Notice, Event, PublicPage, InstitutionSettings


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'notice_type', 'is_published', 'published_at', 'created_at')
    list_filter = ('notice_type', 'is_published')
    search_fields = ('title', 'content')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'location', 'is_published')
    list_filter = ('is_published',)
    search_fields = ('title', 'description')


@admin.register(PublicPage)
class PublicPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published', 'created_at')
    list_filter = ('is_published',)
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(InstitutionSettings)
class InstitutionSettingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'website', 'established_year')
    search_fields = ('name',)