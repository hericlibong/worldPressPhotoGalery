# webapp/urls.py  OU  webapp/gallery/urls.py (selon ta structuration)

from django.contrib import admin
from photoquiz.views import QuizListView, quiz_detail_view, quiz_final_view
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # L’URLConf de ton app PICTURES
    path('', include('pictures.urls')),  
    
    # L’URLConf de ton app AUTH
    path('', include('authentication.urls')),

    # L’URLConf star_ratings
    path('ratings/', include('star_ratings.urls', namespace='ratings')),

     path('quiz/<str:slug>/<int:event_number>/', quiz_detail_view, name = 'quiz-detail'),
    path('quiz/', QuizListView.as_view(), name='quiz-list'),
    path('quiz_score/<str:slug>/', quiz_final_view, name = 'final-score')
]
