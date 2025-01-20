from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'published_date', 'display_cover_thumbnail')
    list_filter = ('author', 'published_date')
    search_fields = ('title', 'author', 'isbn', 'description')
    readonly_fields = (
        'created_at', 'updated_at', 'enriched_data',
        'display_cover', 'display_enriched_info'
    )
    ordering = ('-created_at',)
    date_hierarchy = 'published_date'
    
    def display_cover_thumbnail(self, obj):
        """Displays a thumbnail of the book cover in the list view."""
        if obj.enriched_data and obj.enriched_data.get('image_links', {}).get('thumbnail'):
            return format_html(
                '<img src="{}" height="50"/>',
                obj.enriched_data['image_links']['thumbnail']
            )
        return "No cover"
    display_cover_thumbnail.short_description = 'Cover'
    
    def display_cover(self, obj):
        """Displays a larger version of the book cover in the detail view."""
        if obj.enriched_data and obj.enriched_data.get('image_links', {}).get('thumbnail'):
            return format_html(
                '<img src="{}" height="200"/>',
                obj.enriched_data['image_links']['thumbnail']
            )
        return "No cover available"
    display_cover.short_description = 'Book Cover'
    
    def display_enriched_info(self, obj):
        """Displays formatted enriched information."""
        if not obj.enriched_data:
            return "No enriched data available"
            
        info = []
        
        # Add basic information
        if obj.enriched_data.get('subtitle'):
            info.append(f"<strong>Subtitle:</strong> {obj.enriched_data['subtitle']}")
        
        if obj.enriched_data.get('authors'):
            info.append(f"<strong>Authors:</strong> {', '.join(obj.enriched_data['authors'])}")
            
        if obj.enriched_data.get('publisher'):
            info.append(f"<strong>Publisher:</strong> {obj.enriched_data['publisher']}")
            
        if obj.enriched_data.get('published_date'):
            info.append(f"<strong>Publication Date:</strong> {obj.enriched_data['published_date']}")
            
        if obj.enriched_data.get('page_count'):
            info.append(f"<strong>Page Count:</strong> {obj.enriched_data['page_count']}")
            
        if obj.enriched_data.get('categories'):
            info.append(f"<strong>Categories:</strong> {', '.join(obj.enriched_data['categories'])}")
            
        # Add rating if available
        if obj.enriched_data.get('average_rating'):
            stars = '⭐' * int(float(obj.enriched_data['average_rating']))
            info.append(f"<strong>Rating:</strong> {stars} ({obj.enriched_data['average_rating']})")
            if obj.enriched_data.get('ratings_count'):
                info.append(f"<strong>Number of Ratings:</strong> {obj.enriched_data['ratings_count']}")
        
        # Add description if available
        if obj.enriched_data.get('description'):
            info.append(f"<strong>Description:</strong><br>{obj.enriched_data['description']}")
        
        # Add links
        links = []
        if obj.enriched_data.get('preview_link'):
            links.append(
                f'<a href="{obj.enriched_data["preview_link"]}" target="_blank">Book Preview</a>'
            )
        if obj.enriched_data.get('info_link'):
            links.append(
                f'<a href="{obj.enriched_data["info_link"]}" target="_blank">More Information</a>'
            )
        
        if links:
            info.append(f"<strong>Links:</strong> {' | '.join(links)}")
        
        return mark_safe('<br>'.join(info))
    display_enriched_info.short_description = 'Enriched Information'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'author', 'isbn', 'description', 'published_date')
        }),
        ('Enriched Data', {
            'fields': ('display_cover', 'display_enriched_info'),
            'description': 'Data retrieved from Google Books API'
        }),
        ('Technical Data', {
            'fields': ('enriched_data', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
