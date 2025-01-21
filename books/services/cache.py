import json
import logging
from functools import wraps
from typing import Any, Dict, Optional

from django.conf import settings
from django.core.cache import cache
from django_redis import get_redis_connection

logger = logging.getLogger(__name__)


def is_valid_enriched_data(data: Dict[str, Any]) -> bool:
    """
    Validates if the enriched data is valid before caching.

    Args:
        data: Dictionary with enriched data

    Returns:
        bool indicating if the data is valid
    """
    if not data:
        return False

    # Check required fields
    required_fields = ["title", "authors"]
    if not all(data.get(field) for field in required_fields):
        return False

    # Check if data is not just empty test values
    if data.get("title") == "Test Book" and data.get("authors") == ["Test Author"]:
        return False

    return True


def cache_book_info(func):
    """Decorator to cache book information."""

    @wraps(func)
    def wrapper(isbn: str) -> Optional[Dict[str, Any]]:
        cache_key = f"book:{isbn}"
        logger.info(f"Checking cache for key: {cache_key}")

        try:
            redis_client = get_redis_connection("default")
            logger.info(f"Current Redis keys: {redis_client.keys('*')}")

            cached_data = cache.get(cache_key)

            if cached_data is not None:
                # If cached data is not valid, invalidate the cache
                if not is_valid_enriched_data(cached_data):
                    logger.warning(
                        f"Invalid cached data found for ISBN {isbn}. Invalidating cache."
                    )
                    cache.delete(cache_key)
                    redis_client.delete(f"direct:{cache_key}")
                    cached_data = None
                else:
                    logger.info(f"Cache HIT for {cache_key}")
                    return cached_data

            logger.info(f"Cache MISS for {cache_key}. Fetching data from API.")
            result = func(isbn)

            if result and is_valid_enriched_data(result):
                logger.info(f"Caching valid data for ISBN {isbn}")
                cache.set(
                    cache_key, result, timeout=getattr(settings, "CACHE_TTL", 86400)
                )

                verification = cache.get(cache_key)
                logger.info(
                    f"Cache verification - Key exists: {verification is not None}"
                )

                redis_client.set(f"direct:{cache_key}", json.dumps(result), ex=86400)

                logger.info(f"After caching - Redis keys: {redis_client.keys('*')}")
            else:
                logger.warning(
                    f"Invalid or empty data received for ISBN {isbn}. Not caching."
                )

            return result

        except Exception as e:
            logger.error(f"Cache error: {str(e)}", exc_info=True)
            return func(isbn)

    return wrapper
