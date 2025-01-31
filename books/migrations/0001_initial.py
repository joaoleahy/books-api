# Generated by Django 4.2.18 on 2025-01-17 20:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        help_text="Book title",
                        max_length=200,
                        validators=[django.core.validators.MinLengthValidator(1)],
                    ),
                ),
                (
                    "author",
                    models.CharField(
                        help_text="Book author",
                        max_length=200,
                        validators=[django.core.validators.MinLengthValidator(1)],
                    ),
                ),
                (
                    "isbn",
                    models.CharField(
                        help_text="Book ISBN (10 or 13 digits)",
                        max_length=13,
                        unique=True,
                        validators=[django.core.validators.MinLengthValidator(10)],
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, help_text="Book description"),
                ),
                ("published_date", models.DateField(help_text="Publication date")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "enriched_data",
                    models.JSONField(
                        blank=True, help_text="Enriched book data", null=True
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
                "indexes": [
                    models.Index(fields=["isbn"], name="books_book_isbn_54becd_idx"),
                    models.Index(fields=["title"], name="books_book_title_d3218d_idx"),
                    models.Index(
                        fields=["author"], name="books_book_author_b941fe_idx"
                    ),
                ],
            },
        ),
    ]
