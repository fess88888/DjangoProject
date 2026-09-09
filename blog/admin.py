from django.contrib import admin
from .models import BlogPost

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "created_at", "views_count")
    list_filter = ("is_published",)
    search_fields = ("title", "content")
    readonly_fields = ("created_at", "views_count")  # чтобы нельзя было вручную менять
    date_hierarchy = "created_at"
