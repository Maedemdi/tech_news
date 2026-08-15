from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('news', views.NewsViewset)
router.register('tags', views.TagViewset)

urlpatterns = [
    path('', include(router.urls)),
]
