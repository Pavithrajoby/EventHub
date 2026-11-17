from django.contrib import admin
from .models import Category, Event, Registration, UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'organizer', 'start_time', 'capacity', 'registered_count', 'is_past')
    list_filter = ('category', 'start_time', 'created_at')
    search_fields = ('title', 'description', 'location')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'start_time'

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'ticket_id', 'tickets_count', 'registered_at', 'status', 'is_used')
    list_filter = ('status', 'is_used', 'registered_at')
    search_fields = ('user__username', 'user__email', 'event__title')
