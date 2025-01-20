import requests
from typing import Optional, Dict, Any
from functools import wraps
from django.core.cache import cache
from django.conf import settings
import logging
import json
from django_redis import get_redis_connection

logger = logging.getLogger(__name__)

def cache_book_info(func):
    """Decorator to cache book information."""
    @wraps(func)
    def wrapper(isbn: str) -> Optional[Dict[str, Any]]:
        cache_key = f'book:{isbn}'  # Padrão simples e consistente
        logger.info(f"Checking cache for key: {cache_key}")
        
        try:
            cached_data = cache.get(cache_key)
            logger.info(f"Cache lookup result for {cache_key}: {'HIT' if cached_data else 'MISS'}")
            
            if cached_data is not None:
                return cached_data
            
            logger.info(f"Fetching data from API for ISBN {isbn}")
            result = func(isbn)
            
            if result:
                logger.info(f"Caching data for ISBN {isbn}")
                cache.set(
                    cache_key,
                    result,
                    timeout=getattr(settings, 'CACHE_TTL', 86400)
                )
            else:
                logger.warning(f"No data to cache for ISBN {isbn}")
                
            return result
            
        except Exception as e:
            logger.error(f"Cache error: {str(e)}", exc_info=True)
            return func(isbn)
    
    return wrapper


class BookEnrichmentService:
    """Service for enriching book data using Google Books API."""
    
    GOOGLE_BOOKS_API_URL = 'https://www.googleapis.com/books/v1/volumes'
    
    @staticmethod
    @cache_book_info
    def get_book_info(isbn: str) -> Optional[Dict[str, Any]]:
        """
        Fetches additional book information using Google Books API.
        
        Args:
            isbn: Book ISBN
            
        Returns:
            Dict with book information or None if not found
        """
        try:
            logger.info(f"Making API request for ISBN: {isbn}")
            params = {'q': f'isbn:{isbn}'}
            response = requests.get(BookEnrichmentService.GOOGLE_BOOKS_API_URL, params=params)
            response.raise_for_status()
            
            try:
                data = response.json()
                logger.info("Successfully parsed API response")
            except (ValueError, TypeError) as e:
                logger.error(f"Error parsing JSON response: {e}")
                return None
            
            if data.get('totalItems', 0) == 0:
                logger.warning(f"No books found for ISBN: {isbn}")
                return None
            
            volume_info = data['items'][0]['volumeInfo']
            logger.info(f"Successfully retrieved book data for ISBN: {isbn}")
            
            return {
                'title': volume_info.get('title'),
                'subtitle': volume_info.get('subtitle'),
                'authors': volume_info.get('authors', []),
                'publisher': volume_info.get('publisher'),
                'published_date': volume_info.get('publishedDate'),
                'description': volume_info.get('description'),
                'page_count': volume_info.get('pageCount'),
                'categories': volume_info.get('categories', []),
                'average_rating': volume_info.get('averageRating'),
                'ratings_count': volume_info.get('ratingsCount'),
                'language': volume_info.get('language'),
                'preview_link': volume_info.get('previewLink'),
                'info_link': volume_info.get('infoLink'),
                'image_links': volume_info.get('imageLinks', {}),
            }
            
        except requests.RequestException as e:
            logger.error(f"Error fetching book information: {e}")
            return None
        except (KeyError, IndexError) as e:
            logger.error(f"Error processing book data: {e}")
            return None 