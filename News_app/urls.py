from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('news-list', views.NewsItemViewSet, basename='news-url')


urlpatterns = [
    path('', include(router.urls))
]
