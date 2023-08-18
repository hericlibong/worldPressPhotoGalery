
from django.contrib import admin
from django.urls import path, include
from pictures.views import RecentPictureAPIView, DateListView, ImageListView, ImageByRatingView, statistics_views, image_search_view, ImageByMediaView
from authentication.views import logout_user, signup_page
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/recent-pictures/', RecentPictureAPIView.as_view(), name = 'recent_pictures'),
    path('home/', DateListView.as_view(), name='home'),
    path('images/<str:date>/', ImageListView.as_view(), name='image_list_by_date'),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    path('login/', LoginView.as_view(
        template_name = 'authentication/login.html',
        redirect_authenticated_user =True),
        name = 'login'),
    path('logout/', logout_user, name = 'logout'),
    path('signup/', signup_page, name = 'signup'),
    path('images_ratings/', ImageByRatingView.as_view(), name='images-ratings'),
    path('home/stats/', statistics_views, name = 'stats' ),
    path('search/', image_search_view, name='image-search'),
    path('image_by_media/', ImageByMediaView.as_view(), name = 'image-media' )

]
