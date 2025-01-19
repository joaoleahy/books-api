from django.db import models
from django.core.validators import MinLengthValidator
from typing import Dict, Any


class Book(models.Model):
    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(1)],
        help_text="Book title"
    )
    author = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(1)],
        help_text="Book author"
    )
    isbn = models.CharField(
        max_length=13,
        unique=True,
        validators=[MinLengthValidator(10)],
        help_text="Book ISBN (10 or 13 digits)"
    )
    description = models.TextField(
        blank=True,
        help_text="Book description"
    )
    published_date = models.DateField(
        help_text="Publication date"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    enriched_data = models.JSONField(
        null=True,
        blank=True,
        help_text="Enriched book data"
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['isbn']),
            models.Index(fields=['title']),
            models.Index(fields=['author']),
        ]

    def __str__(self) -> str:
        return f"{self.title} by {self.author}"

    def update_enriched_data(self, data: Dict[str, Any]) -> None:
        """Updates the book's enriched data."""
        self.enriched_data = data
        self.save(update_fields=['enriched_data', 'updated_at'])
