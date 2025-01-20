from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'published_date', 'created_at')
    list_filter = ('author', 'published_date')
    search_fields = ('title', 'author', 'isbn', 'description')
    readonly_fields = ('created_at', 'updated_at', 'enriched_data')
    ordering = ('-created_at',)
    date_hierarchy = 'published_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'author', 'isbn', 'description', 'published_date')
        }),
        ('Enriched Data', {
            'fields': ('enriched_data',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
