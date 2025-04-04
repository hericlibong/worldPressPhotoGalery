import pytest
from django.db.utils import IntegrityError
from pictures.models import PhotoGallery
from django.utils.timezone import now
from datetime import timedelta


@pytest.mark.django_db
class TestPhotoGalleryModel:

    def test_str_method_returns_media(self):
        pic = PhotoGallery.objects.create(
            media="The Atlantic",
            sectionTitle="Photos of the Week",
            pubDate=now(),
            pageUrl="https://example.com",
            caption="Test caption",
            location="Paris",
            picture="https://example.com/image.jpg"
        )
        assert str(pic) == "The Atlantic"

    def test_unique_together_constraint(self):
        pic1 = PhotoGallery.objects.create(
            media="CNN",
            sectionTitle="Weekly Photos",
            pubDate=now(),
            pageUrl="https://cnn.com/photo1",
            caption="Same caption",
            location="Berlin",
            picture="https://cnn.com/image1.jpg"
        )
        with pytest.raises(IntegrityError):
            PhotoGallery.objects.create(
                media="CNN",
                sectionTitle="Weekly Photos",
                pubDate=now(),
                pageUrl="https://cnn.com/photo2",
                caption="Same caption",
                location="Berlin",
                picture="https://cnn.com/image1.jpg"
            )

    def test_ordering_by_pubdate(self):
        old = PhotoGallery.objects.create(
            media="Media A",
            sectionTitle="Oldest",
            pubDate=now() - timedelta(days=5),
            pageUrl="https://old.com",
            caption="Old photo",
            location="NY",
            picture="https://old.com/img.jpg"
        )
        new = PhotoGallery.objects.create(
            media="Media B",
            sectionTitle="Newest",
            pubDate=now(),
            pageUrl="https://new.com",
            caption="New photo",
            location="LA",
            picture="https://new.com/img.jpg"
        )
        pics = PhotoGallery.objects.all()
        assert pics.first() == new
