from django.contrib import admin
from core.models import Plan, Image, CustomUser


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_height', 'uploaded_file_url', 'expiring_url')
    list_display_links = ('name', )
    ordering = ('name', )


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('original_size_image', 'user', 'added_on')
    list_display_links = ('original_size_image', )
    ordering = ('added_on', )
