from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('', views.NewsViewset)

urlpatterns = [
    path('', include(router.urls), name='news_list')
]
