from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from ..models import Book
from .serializers import BookSerializer
from ..services import BookEnrichmentService
from typing import Any


@extend_schema(tags=['books'])
class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing books.
    
    Provides CRUD operations and additional endpoints for book management.
    All operations support JSON format and return paginated results where applicable.
    """
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @extend_schema(
        summary="List all books",
        description="Returns a paginated list of all books in the database.",
        responses={200: BookSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new book",
        description="Creates a new book and enriches it with data from Google Books API.",
        responses={201: BookSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve a book",
        description="Returns the details of a specific book.",
        responses={200: BookSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update a book",
        description="Updates a book's information and refreshes enriched data.",
        responses={200: BookSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a book",
        description="Removes a book from the database.",
        responses={204: None}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer: Any) -> None:
        """
        Overrides create method to enrich book data.
        """
        instance = serializer.save()
        self._enrich_book_data(instance)

    def perform_update(self, serializer: Any) -> None:
        """
        Overrides update method to enrich book data.
        """
        instance = serializer.save()
        self._enrich_book_data(instance)

    @extend_schema(
        summary="Refresh book's enriched data",
        description="Manually triggers a refresh of the book's enriched data from Google Books API.",
        responses={
            200: OpenApiExample(
                'Success',
                value={'status': 'Data updated successfully'}
            ),
            400: OpenApiExample(
                'Error',
                value={'error': 'Could not update data'}
            )
        }
    )
    @action(detail=True, methods=['post'])
    def refresh_enriched_data(self, request: Any, pk: Any = None) -> Response:
        """
        Endpoint to manually update a book's enriched data.
        """
        book = get_object_or_404(Book, pk=pk)
        enriched = self._enrich_book_data(book)
        
        if enriched:
            return Response({'status': 'Data updated successfully'})
        return Response(
            {'error': 'Could not update data'},
            status=status.HTTP_400_BAD_REQUEST
        )

    def _enrich_book_data(self, book: Book) -> bool:
        """
        Enriches book data using the enrichment service.
        
        Args:
            book: Book model instance
            
        Returns:
            bool indicating if enrichment was successful
        """
        enriched_data = BookEnrichmentService.get_book_info(book.isbn)
        if enriched_data:
            book.update_enriched_data(enriched_data)
            return True
        return False
