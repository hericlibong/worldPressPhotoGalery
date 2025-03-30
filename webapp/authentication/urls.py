# webapp/authentication/urls.py

from django.urls import path
from django.contrib.auth.views import LoginView
from .views import logout_user, signup_page

urlpatterns = [
    path('login/', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True),
        name='login'
    ),
    path('logout/', logout_user, name='logout'),
    path('signup/', signup_page, name='signup'),
]
