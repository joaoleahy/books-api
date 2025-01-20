from django.core.management.base import BaseCommand
from books.models import Book
from datetime import date


class Command(BaseCommand):
    help = 'Populates the database with sample books'

    def handle(self, *args, **kwargs):
        books_data = [
            {
                'title': 'The Lord of the Rings: The Fellowship of the Ring',
                'author': 'J.R.R. Tolkien',
                'isbn': '9780261103573',
                'description': 'First volume of The Lord of the Rings trilogy',
                'published_date': date(1954, 7, 29),
            },
            {
                'title': 'The Hobbit',
                'author': 'J.R.R. Tolkien',
                'isbn': '9780261102217',
                'description': 'The journey of Bilbo Baggins',
                'published_date': date(1937, 9, 21),
            },
            {
                'title': 'Harry Potter and the Philosopher\'s Stone',
                'author': 'J.K. Rowling',
                'isbn': '9780747532743',
                'description': 'Harry\'s first year at Hogwarts',
                'published_date': date(1997, 6, 26),
            },
            {
                'title': 'Pride and Prejudice',
                'author': 'Jane Austen',
                'isbn': '9780141439518',
                'description': 'A classic of English literature',
                'published_date': date(1813, 1, 28),
            },
            {
                'title': 'The Little Prince',
                'author': 'Antoine de Saint-Exupéry',
                'isbn': '9780156012195',
                'description': 'A story about love and friendship',
                'published_date': date(1943, 4, 6),
            },
        ]

        for book_data in books_data:
            book, created = Book.objects.get_or_create(
                isbn=book_data['isbn'],
                defaults=book_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Book created: {book.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Book already exists: {book.title}')
                ) 