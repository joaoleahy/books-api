from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BookViewSet

router = DefaultRouter()
router.register(r"books", BookViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
