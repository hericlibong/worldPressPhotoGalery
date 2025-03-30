# webapp/pictures/urls.py

from django.urls import path
from .views import (
    RecentPictureAPIView,
    DateListView,
    ImageListView,
    ImageByRatingView,
    statistics_views,
    image_search_view,
    ImageByMediaView
)

urlpatterns = [
    path('api/recent-pictures/', RecentPictureAPIView.as_view(), name='recent_pictures'),
    path('', DateListView.as_view(), name='home'),  # Page d’accueil
    path('images/<str:date>/', ImageListView.as_view(), name='image_list_by_date'),
    path('images_ratings/', ImageByRatingView.as_view(), name='images-ratings'),
    path('home/stats/', statistics_views, name='stats'),
    path('search/', image_search_view, name='image-search'),
    path('image_by_media/', ImageByMediaView.as_view(), name='image-media'),
]
