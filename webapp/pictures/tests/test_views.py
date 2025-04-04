import pytest
from django.urls import reverse
from pictures.models import PhotoGallery
from datetime import datetime
from django.utils.timezone import make_aware

@pytest.mark.django_db
class TestPictureViews:
    def setup_method(self):
        self.picture = PhotoGallery.objects.create(
            media="CNN",
            sectionTitle="Photos of the week",
            pubDate=make_aware(datetime(2025, 4, 1)),
            pageUrl="https://edition.cnn.com/photos-of-the-week",
            caption="A strong caption",
            location="New York",
            author="Jane Doe",
            credits="CNN Photos",
            picture="https://cdn.cnn.com/path/to/photo.jpg",
            pictureEditor="Editor Name"
        )

    def test_recent_picture_api_view(self, client):
        url = reverse("recent_pictures")
        response = client.get(url)
        assert response.status_code == 200
        assert "pictures" in response.json()

    def test_date_list_view(self, client):
        url = reverse("home")
        response = client.get(url)
        assert response.status_code == 200
        assert "date_list" in response.context

    def test_image_list_view(self, client):
        date_str = self.picture.pubDate.strftime('%Y-%m-%d')
        url = reverse("image_list_by_date", kwargs={"date": date_str})
        response = client.get(url)
        assert response.status_code == 200
        assert "image_list" in response.context

    def test_image_by_rating_view(self, client):
        url = reverse("images-ratings")
        response = client.get(url)
        assert response.status_code == 200
        assert "images_by_rating" in response.context

    def test_statistics_view(self, client):
        url = reverse("stats")
        response = client.get(url)
        assert response.status_code == 200
        assert "media_data" in response.context

    def test_image_search_view(self, client):
        url = reverse("image-search")
        response = client.get(url)
        assert response.status_code == 200
        assert "form" in response.context

    def test_image_by_media_view_all(self, client):
        url = reverse("image-media")
        response = client.get(url)
        assert response.status_code == 200
        assert "images_by_media" in response.context
        assert "available_media" in response.context

    def test_image_by_media_view_filtered(self, client):
        url = reverse("image-media") + "?media=CNN"
        response = client.get(url)
        assert response.status_code == 200
        assert "images_by_media" in response.context
        assert "available_media" in response.context

    def test_image_search_view_with_search_field_all(self, client):
        url = reverse("image-search")
        response = client.get(url, {
            "keyword": "CNN",
            "search_field": "all"
        })
        assert response.status_code == 200
        assert "images" in response.context
        assert "results_counts" in response.context

    def test_image_search_view_with_specific_field(self, client):
        url = reverse("image-search")
        response = client.get(url, {
            "keyword": "CNN",
            "search_field": "media"
        })
        assert response.status_code == 200
        assert "images" in response.context
        assert "results_counts" in response.context
