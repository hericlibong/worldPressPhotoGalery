from django.contrib import admin
from pictures.models import PhotoGallery

class PhotoGalleryAdmin(admin.ModelAdmin):
    list_display = ('media', 'pubDate', 'sectionTitle', 'author', 'credits', 'pictureEditor',)
    search_fields = ('pubDate', 'media',)
    list_per_page = 10

admin.site.register(PhotoGallery, PhotoGalleryAdmin)


# Register your models here.
