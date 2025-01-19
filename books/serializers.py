from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'author',
            'isbn',
            'description',
            'published_date',
            'created_at',
            'updated_at',
            'enriched_data',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'enriched_data']

    def validate_isbn(self, value: str) -> str:
        """
        Validates ISBN by removing hyphens and checking length.
        """
        # Remove hyphens from ISBN
        isbn = value.replace('-', '')
        
        # Check if ISBN has 10 or 13 digits
        if len(isbn) not in [10, 13]:
            raise serializers.ValidationError(
                'ISBN must be 10 or 13 digits long.'
            )
        
        return isbn 