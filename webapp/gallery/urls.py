# webapp/urls.py  OU  webapp/gallery/urls.py (selon ta structuration)

from django.contrib import admin

from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # L’URLConf de ton app PICTURES
    path('', include('pictures.urls')),  
    
    # L’URLConf de ton app AUTH
    path('', include('authentication.urls')),

    # L’URLConf star_ratings
    path('ratings/', include('star_ratings.urls', namespace='ratings')),

]
