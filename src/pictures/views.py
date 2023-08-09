from typing import Any, Dict, Tuple
#from django.db.models.query import _BaseQuerySet, QuerySet
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from rest_framework.views import APIView
from pictures.models import PhotoGallery
from django.db.models import Count, F, Subquery, OuterRef

from datetime import datetime                                                                               

from django.views.generic import ListView

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
#from django.contrib.humanize.templatetags.humanize import naturaltime
from django.utils import timezone





### API interface views ###

class RecentPictureAPIView(APIView):
    def get(self, request, format=None):
        pictures = PhotoGallery.objects.order_by('-pubDate')
        data = {
        'pictures': list(pictures.values())
        }
        return JsonResponse(data)


#### Class based views ####

class DateListView(ListView):
    model = PhotoGallery
    template_name = 'pictures/date_list.html' 
    context_object_name = 'date_list' 

    def get_queryset(self):
        date_counts = PhotoGallery.objects.order_by('-pubDate').values('pubDate').distinct().annotate(total_photos=Count('id'))
        first_images = PhotoGallery.objects.filter(pubDate=OuterRef('pubDate')).order_by('id').values('picture')[:1]
        date_list = date_counts.annotate(first_image=Subquery(first_images))
        return date_list
    

 


class ImageListView(ListView):
    model = PhotoGallery
    template_name = 'pictures/images_list.html' 
    context_object_name = 'image_list'
    paginate_by = 10 # Nombre d'objects/images par page

    def get_queryset(self): 
        date_str = self.kwargs['date']
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        queryset = PhotoGallery.objects.raw(f"SELECT * FROM pictures_photogallery WHERE DATE(pubDate) = %s", [date])
        return queryset

    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date_str = self.kwargs['date']
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        formatted_date = date.strftime('%a %d %b %Y')
        context['date'] = formatted_date
        return context
    


class ImageByRatingView(ListView):
    model = PhotoGallery
    template_name = 'pictures/images_by_rating.html'
    context_object_name = 'images_by_rating'
    paginate_by = 10

    def get_queryset(self):
        return PhotoGallery.objects.filter(ratings__isnull=False).order_by('-ratings__average')
        


    







