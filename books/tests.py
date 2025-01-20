from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Book
from .services import BookEnrichmentService, cache_book_info
from datetime import date
from unittest.mock import patch, Mock
import requests
from django.core.cache import cache


class BookModelTests(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="The Lord of the Rings",
            author="J.R.R. Tolkien",
            isbn="9780261103573",
            description="An epic story",
            published_date=date(1954, 7, 29)
        )

    def test_book_creation(self):
        self.assertTrue(isinstance(self.book, Book))
        self.assertEqual(str(self.book), "The Lord of the Rings by J.R.R. Tolkien")

    def test_update_enriched_data(self):
        test_data = {"test": "data"}
        self.book.update_enriched_data(test_data)
        self.assertEqual(self.book.enriched_data, test_data)


class BookAPITests(APITestCase):
    def setUp(self):
        self.book_data = {
            "title": "The Hobbit",
            "author": "J.R.R. Tolkien",
            "isbn": "9780261102217",
            "description": "An unexpected journey",
            "published_date": "1937-09-21"
        }
        self.book = Book.objects.create(**self.book_data)

    def test_list_books(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_book(self):
        url = reverse('book-list')
        data = {
            "title": "The Silmarillion",
            "author": "J.R.R. Tolkien",
            "isbn": "9780261102422",
            "description": "The history of Middle-earth",
            "published_date": "1977-09-15"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_create_book_invalid_data(self):
        url = reverse('book-list')
        data = {
            "title": "",  # Empty title
            "author": "J.R.R. Tolkien",
            "isbn": "invalid-isbn",
            "description": "Test",
            "published_date": "1977-09-15"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)
        self.assertIn('isbn', response.data)

    def test_get_book_detail(self):
        url = reverse('book-detail', args=[self.book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book_data['title'])

    def test_get_nonexistent_book(self):
        url = reverse('book-detail', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_book(self):
        url = reverse('book-detail', args=[self.book.id])
        data = {
            "title": "Updated Title",
            "author": self.book_data['author'],
            "isbn": self.book_data['isbn'],
            "description": "Updated description",
            "published_date": self.book_data['published_date']
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Title")

    def test_delete_book(self):
        url = reverse('book-detail', args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    @patch('books.services.BookEnrichmentService.get_book_info')
    def test_refresh_enriched_data(self, mock_get_book_info):
        mock_data = {
            'title': 'The Hobbit',
            'authors': ['J.R.R. Tolkien'],
            'description': 'Enriched version'
        }
        mock_get_book_info.return_value = mock_data

        url = reverse('book-refresh-enriched-data', args=[self.book.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.enriched_data, mock_data)

    @patch('books.services.BookEnrichmentService.get_book_info')
    def test_refresh_enriched_data_failure(self, mock_get_book_info):
        mock_get_book_info.return_value = None
        url = reverse('book-refresh-enriched-data', args=[self.book.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BookEnrichmentServiceTests(TestCase):
    def setUp(self):
        cache.clear()
        self.isbn = "9780261102217"

    @patch('requests.get')
    def test_get_book_info_success(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            'items': [{
                'volumeInfo': {
                    'title': 'Test Book',
                    'authors': ['Test Author'],
                    'description': 'Test Description'
                }
            }],
            'totalItems': 1
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = BookEnrichmentService.get_book_info(self.isbn)
        self.assertIsNotNone(result)
        self.assertEqual(result['title'], 'Test Book')

    @patch('requests.get')
    def test_get_book_info_no_results(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {'totalItems': 0}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = BookEnrichmentService.get_book_info(self.isbn)
        self.assertIsNone(result)

    @patch('requests.get')
    def test_get_book_info_request_error(self, mock_get):
        mock_get.side_effect = requests.RequestException()
        result = BookEnrichmentService.get_book_info(self.isbn)
        self.assertIsNone(result)

    @patch('requests.get')
    def test_get_book_info_invalid_response(self, mock_get):
        mock_response = Mock()
        mock_response.json.side_effect = ValueError()
        mock_get.return_value = mock_response

        result = BookEnrichmentService.get_book_info(self.isbn)
        self.assertIsNone(result)

    def test_cache_decorator(self):
        test_data = {'test': 'data'}
        
        @cache_book_info
        def mock_get_info(isbn):
            return test_data

        result1 = mock_get_info(self.isbn)
        self.assertEqual(result1, test_data)

        result2 = mock_get_info(self.isbn)
        self.assertEqual(result2, test_data)

        cached_data = cache.get(f'book_info_{self.isbn}')
        self.assertEqual(cached_data, test_data)
