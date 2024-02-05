from django.contrib import admin
from .models import Board

# Register your models here.
@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ("title", "content", "created_at", "updated_at", "author")
    list_filter = ("created_at", "updated_at")
    search_fields = ("title", "content", "author__username")
    date_hierarchy = "created_at"
    ordering = ("created_at",)