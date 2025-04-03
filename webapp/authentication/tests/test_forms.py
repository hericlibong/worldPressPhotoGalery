import pytest
from authentication.forms import SignupForm, LoginForm
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_signup_form_valid_data():
    form = SignupForm(data={
        "username": "testuser",
        "email" : "testemail@email.com",
        "first_name" : "Test",
        "last_name" : "User",
        "password1" : "TestPassword123",
        "password2" : "TestPassword123",

    })
    assert form.is_valid(), form.errors

@pytest.mark.django_db
def test_signup_form_invalid_password_mismatch():
    form = SignupForm(data={
        "username": "newuser",
        "email": "newuser@example.com",
        "first_name": "New",
        "last_name": "User",
        "password1": "StrongPass123!",
        "password2": "WrongPass456!",
    })
    assert not form.is_valid()
    assert "password2" in form.errors


def test_login_form_valid_data():
    form = LoginForm(data={
        "username": "testuser",
        "password": "testpassword",
    })
    assert form.is_valid(), form.errors


def test_login_form_missing_username():
    form = LoginForm(data={
        "password": "testpassword",
    })
    assert not form.is_valid()
    assert "username" in form.errors
