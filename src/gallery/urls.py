
from django.contrib import admin
from django.urls import path, include
from pictures.views import RecentPictureAPIView, DateListView, ImageListView, ImageByRatingView
from authentication.views import logout_user
from django.contrib.auth.views import LoginView
from authentication.views import signup_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/recent-pictures/', RecentPictureAPIView.as_view(), name = 'recent_pictures'),
    path('home/', DateListView.as_view(), name='home'),
    path('images/<str:date>/', ImageListView.as_view(), name='image_list_by_date'),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    #path('login/', LoginPage.as_view(), name='login'),
    path('login/', LoginView.as_view(
        template_name = 'authentication/login.html',
        redirect_authenticated_user =True),
        name = 'login'),
    #path('login/', login_page, name = 'login'),
    path('logout/', logout_user, name = 'logout'),
    #path('logout/', LogoutView.as_view(), name = 'logout'),
    path('signup/', signup_page, name = 'signup'),
    path('images_ratings/', ImageByRatingView.as_view(), name='images-ratings')

]
