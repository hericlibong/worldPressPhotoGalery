import pytest
from django.urls import reverse, NoReverseMatch
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


@pytest.mark.django_db
class TestSignupView:

    def test_signup_get_request_returns_200(self, client):
        response = client.get(reverse("signup"))
        assert response.status_code == 200
        assert "form" in response.context

    def test_signup_post_invalid_data_does_not_create_user(self, client):
        data = {"username": "", "password1": "", "password2": ""}
        response = client.post(reverse("signup"), data)
        assert response.status_code == 200
        assert User.objects.count() == 0
        assert "form" in response.context
        assert response.context["form"].errors

    def test_signup_post_valid_data_creates_user_and_redirects(self, client):
        data = {
            "username": "testuser",
            "password1": "VeryStrongPass!123",
            "password2": "VeryStrongPass!123"
        }
        response = client.post(reverse("signup"), data)
        assert response.status_code == 302  # Redirection
        assert response.url == settings.LOGIN_REDIRECT_URL
        assert User.objects.filter(username="testuser").exists()


@pytest.mark.django_db
class TestLogoutView:

    def test_logout_redirects_to_home_raises_error_if_home_not_defined(self, client, django_user_model):
        # Création d'un utilisateur et login
        user = django_user_model.objects.create_user(username="tempuser", password="temp1234")
        client.login(username="tempuser", password="temp1234")

        response = client.get(reverse("logout"))
        assert response.status_code == 302

        # Si "home" n'est pas défini, un reverse("home") doit échouer
        with pytest.raises(NoReverseMatch):
            reverse("home")


@pytest.mark.django_db
class TestLogoutView:

    def test_logout_logs_user_out_and_redirects(self, client, django_user_model):
        user = django_user_model.objects.create_user(username="tempuser", password="temp1234")
        client.login(username="tempuser", password="temp1234")

        response = client.get(reverse("logout"))

        assert response.status_code == 302
        # l’utilisateur doit être déconnecté après cette requête
        assert "_auth_user_id" not in client.session
