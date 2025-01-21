import json
import logging
from functools import wraps
from typing import Any, Dict, Optional

from django.conf import settings
from django.core.cache import cache
from django_redis import get_redis_connection

logger = logging.getLogger(__name__)


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
            logger.info(
                f"Cache lookup result for {cache_key}: {'HIT' if cached_data else 'MISS'}"
            )

            if cached_data is not None:
                return cached_data

            logger.info(f"Fetching data from API for ISBN {isbn}")
            result = func(isbn)

            if result:
                logger.info(f"Caching data for ISBN {isbn}")
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
                logger.warning(f"No data to cache for ISBN {isbn}")

            return result

        except Exception as e:
            logger.error(f"Cache error: {str(e)}", exc_info=True)
            return func(isbn)

    return wrapper
