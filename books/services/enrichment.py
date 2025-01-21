import logging
import os
from typing import Any, Dict, Optional

import requests
from django.conf import settings

from .cache import cache_book_info

logger = logging.getLogger(__name__)


class BookEnrichmentService:
    """Service for enriching book data using Google Books API."""

    GOOGLE_BOOKS_API_URL = os.getenv("GOOGLE_BOOKS_API_URL")

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
            params = {"q": f"isbn:{isbn}"}
            response = requests.get(
                BookEnrichmentService.GOOGLE_BOOKS_API_URL, params=params
            )
            response.raise_for_status()

            try:
                data = response.json()
                logger.info("Successfully parsed API response")
            except (ValueError, TypeError) as e:
                logger.error(f"Error parsing JSON response: {e}")
                return None
            if not data.get("totalItems", 0) or "items" not in data:
                return None

            volume_info = data["items"][0]["volumeInfo"]
            logger.info(f"Successfully retrieved book data for ISBN: {isbn}")

            return {
                "title": volume_info.get("title"),
                "subtitle": volume_info.get("subtitle"),
                "authors": volume_info.get("authors", []),
                "publisher": volume_info.get("publisher"),
                "published_date": volume_info.get("publishedDate"),
                "description": volume_info.get("description"),
                "page_count": volume_info.get("pageCount"),
                "categories": volume_info.get("categories", []),
                "average_rating": volume_info.get("averageRating"),
                "ratings_count": volume_info.get("ratingsCount"),
                "language": volume_info.get("language"),
                "preview_link": volume_info.get("previewLink"),
                "info_link": volume_info.get("infoLink"),
                "image_links": volume_info.get("imageLinks", {}),
            }

        except requests.RequestException as e:
            logger.error(f"Error fetching book information: {e}")
            return None
        except (KeyError, IndexError) as e:
            logger.error(f"Error processing book data: {e}")
            return None
