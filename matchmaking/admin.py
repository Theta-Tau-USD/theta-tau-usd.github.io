from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, BrotherProfile, PNMProfile, Badge


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin interface for CustomUser model"""
    list_display = ['username', 'email', 'role', 'first_name', 'last_name', 'is_staff']
    list_filter = ['role', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    """Admin interface for Badge model"""
    list_display = ['name', 'pillar', 'icon_image', 'order']
    list_filter = ['pillar']
    search_fields = ['name', 'description']
    ordering = ['pillar', 'order', 'name']


@admin.register(BrotherProfile)
class BrotherProfileAdmin(admin.ModelAdmin):
    """Admin interface for BrotherProfile model"""
    list_display = ['name', 'year', 'major', 'user', 'badge_count', 'created_at']
    list_filter = ['year', 'created_at', 'badges']
    search_fields = ['name', 'major', 'description']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['badges']
    
    def badge_count(self, obj):
        return obj.badges.count()
    badge_count.short_description = 'Badges'


@admin.register(PNMProfile)
class PNMProfileAdmin(admin.ModelAdmin):
    """Admin interface for PNMProfile model"""
    list_display = ['name', 'year', 'major', 'user', 'created_at']
    list_filter = ['year', 'created_at']
    search_fields = ['name', 'major', 'description']
    readonly_fields = ['created_at', 'updated_at']
