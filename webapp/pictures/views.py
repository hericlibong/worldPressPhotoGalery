import json
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from pictures.forms import ImageSearchForm
from pictures.models import PhotoGallery
from django.db.models import Count, Subquery, OuterRef, Q
from datetime import datetime
from django.views.generic import ListView


# API interface views
class RecentPictureAPIView(APIView):
    def get(self, request, format=None):
        pictures = PhotoGallery.objects.order_by('-pubDate')
        data = {
            'pictures': list(pictures.values())
        }
        return JsonResponse(data)


# Class based views
class DateListView(ListView):
    model = PhotoGallery
    template_name = 'pictures/date_list.html'
    context_object_name = 'date_list'
    paginate_by = 9

    def get_queryset(self):
        date_counts = PhotoGallery.objects.order_by('-pubDate').values('pubDate').distinct().annotate(total_photos=Count('id'))
        first_images = PhotoGallery.objects.filter(pubDate=OuterRef('pubDate')).order_by('id').values('picture')[:1]
        date_list = date_counts.annotate(first_image=Subquery(first_images))
        return date_list


class ImageListView(ListView):
    model = PhotoGallery
    template_name = 'pictures/images_list.html'
    context_object_name = 'image_list'
    paginate_by = 10  # Nombre d'objects/images par page

    def get_queryset(self):
        date_str = self.kwargs['date']
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        queryset = PhotoGallery.objects.raw("SELECT * FROM pictures_photogallery WHERE DATE(pubDate) = %s", [date])
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


# Statistics views
def statistics_views(request):
    media_counts = PhotoGallery.objects.values('media').annotate(count=Count('id'))
    media_data = [{'media': item['media'], 'count': item['count']} for item in media_counts]

    context = {
        'media_data': json.dumps(media_data),
    }
    return render(request, 'pictures/stats.html', context)


class ImageByMediaView(ListView):
    model = PhotoGallery
    template_name = 'pictures/images_by_media.html'
    context_object_name = 'images_by_media'
    paginate_by = 10

    def get_queryset(self):
        selected_media = self.request.GET.get('media')
        if selected_media:
            return PhotoGallery.objects.filter(media=selected_media)
        else:
            return PhotoGallery.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_media = self.request.GET.get('media')

        if selected_media:
            images_by_media = PhotoGallery.objects.filter(media=selected_media)
            context['images_by_media_count'] = images_by_media.count()  # Ajoutez cette ligne au contexte

        available_media = PhotoGallery.objects.order_by('media').values_list('media', flat=True).distinct()
        context['available_media'] = available_media
        return context


# browse pictures dropdown menu
def image_search_view(request):
    form = ImageSearchForm(request.GET)
    images = []
    results_counts = 0

    if form.is_valid():
        keyword = form.cleaned_data.get('keyword')
        search_field = form.cleaned_data.get('search_field')

        # Vérification si le champ de recherche est sélectionné
        if keyword:
            if search_field == 'all':
                # Utilisation de Q pour rechercher dans tous les champs pertinents
                filter_q = Q(caption__icontains=keyword) | Q(media__icontains=keyword) | Q(credits__icontains=keyword) | Q(author__icontains=keyword) | Q(location__icontains=keyword)
                images = PhotoGallery.objects.filter(filter_q)
            else:
                # Utilisation du champ de recherche sélectionné pour filtrer les images
                filter_kwargs = {f'{search_field}__icontains': keyword}
                images = PhotoGallery.objects.filter(**filter_kwargs)

            results_counts = len(images)

    context = {
        'form': form,
        'images': images,
        'results_counts': results_counts
    }

    return render(request, 'pictures/image_search.html', context)
